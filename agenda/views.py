from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from agenda.models import Agendamento
from datetime import datetime, timedelta, time, date
from agenda.serializers import AgendamentoSerializer
from rest_framework import serializers
from django.utils import timezone
# Create your views here.

@api_view(http_method_names=["GET", "PATCH", "DELETE"])
def agendamento_detail(request, id):
    #trazer agendamento detalhado:
    obj = get_object_or_404(Agendamento, id=id)
    if request.method == "GET":
      
      serializer = AgendamentoSerializer(obj)
      return JsonResponse(serializer.data)
    #editar agendamento:
    if request.method == "PATCH":
      serializer = AgendamentoSerializer(obj, data=request.data, partial=True)
      if obj.cancelamento_agendamento == True:
         raise serializers.ValidationError("Agendamento já foi cancelado, impossível alterar")
      
      if not serializer.is_valid():
        return JsonResponse(serializer.errors, status=400)
      
      dt = datetime.strptime(request.data['data_horario'], "%Y-%m-%d %H:%M:%S")
      todos_agendamentos = Agendamento.objects.filter(cancelamento_agendamento=False)

      for agendamento in todos_agendamentos:
          if obj.id != agendamento.id: 
            agendamento.data_horario = agendamento.data_horario.replace(tzinfo=None)          
            if dt == agendamento.data_horario:
             raise serializers.ValidationError("Horário já ocupado")
        
      serializer.save()
      return JsonResponse(serializer.data, status=200)
      
    #cancelar agendamento:
    if request.method == "DELETE":
      obj.cancelamento_agendamento = True
      obj.save()
      return Response(status=204)
  
  
@api_view(http_method_names=["GET", "POST"])
def agendamento_list(request):
    if request.method == "GET":
      qs = Agendamento.objects.filter(cancelamento_agendamento=False)
      serializer = AgendamentoSerializer(qs, many=True)
      return JsonResponse(serializer.data, safe=False)
    
    if request.method == "POST":
       data = request.data
       serializer = AgendamentoSerializer(data=data)
       print(data)
       
       if not serializer.is_valid():
        return JsonResponse(serializer.errors, status=400)
         
       agendamentos_cliente = Agendamento.objects.filter(email_cliente = data['email_cliente'])
       dt = datetime.strptime(data['data_horario'], "%Y-%m-%d %H:%M:%S")
                
       for agendamento in agendamentos_cliente:            
                if agendamento.data_horario.date() == dt.date():
                  raise serializers.ValidationError("Apenas um agendamento por dia")
        
       todos_agendamentos = Agendamento.objects.filter(cancelamento_agendamento=False)
       for agendamento in todos_agendamentos:
           agendamento.data_horario = agendamento.data_horario.replace(tzinfo=None)
           
           if dt == agendamento.data_horario:
             raise serializers.ValidationError("Horário já ocupado")
           
        
       serializer.save()
        
       return JsonResponse(serializer.data, status=201)
       
     
     
@api_view(http_method_names=["GET"])
def horarios_list(request):
  data = request.query_params.get("data")
  data = datetime.fromisoformat(data).date()
  
  #verificar se a data está no passado:
  if data < date.today():
    raise serializers.ValidationError("Não há horários disponíveis no passado!")
  
  #trazer todos os agendamentos para comparação:
  qs = Agendamento.objects.filter(cancelamento_agendamento=False)
 
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
  
  
  
  
  