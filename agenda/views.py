from django.shortcuts import get_object_or_404
from django.core.serializers import serialize
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from agenda.models import Agendamento, Cliente, Fidelidade
from datetime import datetime, timedelta, timezone, date
from agenda.serializers import AgendamentoSerializer, PrestadorSerializer, ClienteSerializer, FidelidadeSerializer
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics, permissions
from django.contrib.auth.models import User
import json


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
def horarios_list(request):
  data = request.query_params.get("data")
  data = datetime.fromisoformat(data).date()
  
  #verificar se a data está no passado:
  if data < date.today():
    raise serializers.ValidationError("Não há horários disponíveis no passado!")
  
  #trazer todos os agendamentos para comparação:
  qs = Agendamento.objects.filter(estado_agendamento = 'CO')
 
  horario = "09:00"
  horario = datetime.strptime(horario, "%H:%M")  
  hr_disp = [] #lista de horários disponíveis a ser populada
  
  
  if data.weekday() < 5: #verifica se for meio da semana
   while horario.hour < 18:
     count = 0
     for ag in qs:
      if ag.data_horario.date()==data and ag.data_horario.hour == horario.hour and ag.data_horario.minute == horario.minute: #verifica se existe algum agendamento no horário corrente da iteração
       count = count+1   
     if count == 0: #se não existir, popular lista de horários disponíveis
      hr = f"{data} {horario.hour}:{horario.minute}"
      hr = datetime.strptime(hr, "%Y-%m-%d %H:%M")
      hr_disp.append(hr)
      
     horario = horario + timedelta(minutes = 30)
     if horario.hour == 12: #verifica se o horário está dentro do almoço
       horario = horario + timedelta(hours = 1) #se almoço, pula 1h
       
  elif data.weekday() == 5: #verifica se é sábado
    while horario.hour < 13:
      count = 0
      for ag in qs:
       if ag.data_horario.date()==data and ag.data_horario.hour == horario.hour and ag.data_horario.minute == horario.minute:
        count = count+1   
      if count == 0:
       hr = f"{data} {horario.hour}:{horario.minute}"
       hr = datetime.strptime(hr, "%Y-%m-%d %H:%M")
       hr_disp.append(hr)
      
      horario = horario + timedelta(minutes = 30)
    
  elif data.weekday() == 6: #verifica se é domingo
    raise serializers.ValidationError("Sem horários disponíveis no domingo")      
    
  return JsonResponse(hr_disp, safe=False)    #retorna lista de horários disponíveis
  
  
  
  
  