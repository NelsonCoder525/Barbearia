from django.shortcuts import get_object_or_404
from django.core.serializers import serialize
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from agenda.models import Agendamento, Cliente, Fidelidade, Endereco
from datetime import datetime, timedelta, timezone, date
from agenda.serializers import AgendamentoSerializer, PrestadorSerializer, ClienteSerializer, FidelidadeSerializer, EnderecoSerializer
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics, permissions
from django.contrib.auth.models import User
import json
import requests
from agenda.utils import get_horarios_list
from rest_framework import status


# Create your views here.

"""Perimssões:
-Qualquer cliente (autenticado ou não) seja capaz de criar um Agendamento
-Apenas o prestador de serviço pode visualizar todos os agendamentos em sua agenda
-Apenas o prestador de serviço pode manipular os seus agendamentos
"""
class IsOwnerOrCreateOnly(permissions.BasePermission):
  def has_permission(self, request, view):
    if request.method == "POST":
      return True
    username = request.query_params.get("username", None)
    if request.user.username == username:
      return True
    return False
    
class IsPrestador(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    if obj.prestador == request.user:
      return True
    return False
  
class IsSuperUser(permissions.BasePermission):
  def has_permission(self, request, view):
    if request.user.is_superuser == True:
      return True
    return False

class AgendamentoDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Agendamento.objects.all()
  serializer_class = AgendamentoSerializer
  permission_classes = [IsSuperUser]

class AgendamentoList(generics.ListCreateAPIView):
  queryset = Agendamento.objects.filter(estado_agendamento = 'CO')  
  serializer_class = AgendamentoSerializer
  permission_classes = [IsOwnerOrCreateOnly]
  
  def get_queryset(self):
    username = self.request.query_params.get("username", None)
    queryset = Agendamento.objects.filter(prestador__username = username, estado_agendamento = 'CO')
    
    return queryset
 
class PrestadorList(generics.ListAPIView):    
  serializer_class = PrestadorSerializer
  queryset = User.objects.all()  
  permission_classes = [IsSuperUser]

class ClienteList(generics.ListCreateAPIView):
  serializer_class = ClienteSerializer
  queryset = Cliente.objects.all()  
  permission_classes = [IsSuperUser] 
  
class ClienteDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Cliente.objects.all()
  serializer_class = ClienteSerializer
  permission_classes = [IsSuperUser]
  
class FidelidadeDetail(generics.RetrieveUpdateDestroyAPIView):    
  serializer_class = FidelidadeSerializer
  queryset = Fidelidade.objects.all()
  permission_classes = [IsSuperUser]  

@api_view(http_method_names=["GET"])
def fidelizacoes_list(self):         
    todos_agendamentos = Agendamento.objects.filter(estado_agendamento="EX")
    todos_clientes = Cliente.objects.all()
    todas_fidelizacoes = Fidelidade.objects.all()
    todos_prestadores = User.objects.all()
           
    for clientes in todos_clientes: 
      for agendamento in todos_agendamentos:
          if agendamento.email_cliente == clientes.email: 
            if Fidelidade.objects.all() ==  []: 
              cl = Cliente.objects.filter(email=clientes.email)
              ag = Agendamento.objects.filter(pk=agendamento.pk)
              Fidelidade.objects.create(cliente = cl[0], prestador_fidelidade = agendamento.prestador, agendamento_id = ag[0])
            else:                
              count = 0 
              for fidel in todas_fidelizacoes: 
                if fidel.agendamento_id.pk == agendamento.pk:
                  count +=1 
                
                if count<1:                    
                  cl = Cliente.objects.filter(email=clientes.email)
                  ag = Agendamento.objects.filter(pk=agendamento.pk)
                  Fidelidade.objects.create(cliente = cl[0], prestador_fidelidade = agendamento.prestador, agendamento_id = ag[0])
                  
          fidelizacoes = Fidelidade.objects.all()
          serialized_data = serialize("json", fidelizacoes)
          serialized_data = json.loads(serialized_data)
          
          fidel_list = []
          for fidel in todas_fidelizacoes: 
            fidel_str = f"Fidelização nº{fidel.pk}, Cliente: {fidel.cliente.nome}, Prestador: {fidel.prestador_fidelidade}, Agendamento (ID): {fidel.agendamento_id.pk}" 
            fidel_list.append(fidel_str)  
                    
          display = []
          for client in todos_clientes:
            for prest in todos_prestadores:
              contador = 0
              for fidel in todas_fidelizacoes:
                if fidel.cliente == client and fidel.prestador_fidelidade == prest:
                  contador +=1
              if contador>0:
               display_str = f"Cliente {client.nome} possui {contador} pontos de fidelidade com prestador {prest.username}"
               display.append(display_str)
           
          return JsonResponse(display, safe = False)          
                        

     
@api_view(http_method_names=["GET"])
def horarios_disponiveis(request):
  
  data_param = request.query_params.get('data', None)
  data = datetime.strptime(data_param, '%Y-%m-%d').date()
  horarios = sorted(list(get_horarios_list(data)))

  return Response(horarios)


class EnderecoList(generics.ListCreateAPIView):
  serializer_class = EnderecoSerializer
  queryset = Endereco.objects.all()  
  
@api_view(http_method_names=["GET"])
def healthcheck(request):
  return JsonResponse({"status": "ok"}, status=200)
  
  
  
@api_view(['POST'])
def create_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    
    if not username or not password:
        return Response({'error': 'Usuário e senha são obrigatórios'}, status=status.HTTP_400_BAD_REQUEST)
      
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Usuário já existe'}, status=status.HTTP_400_BAD_REQUEST)
      
    user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
        
    )

    return Response({'message': 'Usuário criado com sucesso!'}, status=status.HTTP_201_CREATED)
  
  