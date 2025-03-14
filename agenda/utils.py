from datetime import datetime, timedelta, timezone, date
from typing import Iterable
from agenda.models import Agendamento, Cliente, Fidelidade
from django.http import JsonResponse
from django.core.serializers import serialize
import requests
from rest_framework import serializers
from agenda.libs import brasil_api, viacep

def get_horarios_list(data: date) -> Iterable[datetime]:
  
  #verificar se a data está no passado:
  if data < date.today():
    raise serializers.ValidationError("Não há horários disponíveis no passado!")
  
  
  #verificar se a data é um feriado:
  if brasil_api.is_feriado(data):
      raise serializers.ValidationError("Feriado, camarada!")
      
  
  else:
  #trazer todos os agendamentos para comparação:
   qs = Agendamento.objects.filter(estado_agendamento = 'CO')
 
   horario = datetime(year=data.year, month=data.month, day = data.day, hour = 9, minute = 0, tzinfo=timezone.utc)
  
   delta = timedelta(minutes=30)
  
   hr_disp = [] #lista de horários disponíveis a ser populada
  
  
   if data.weekday() < 5: #verifica se for meio da semana
    horario_final = datetime(year=data.year, month=data.month, day = data.day, hour = 18, minute = 0, tzinfo=timezone.utc)
    while horario < horario_final:
        if not qs.filter(data_horario=horario).exists():
           hr_disp.append(horario)
        horario = horario + delta
        if horario.hour == 12: #verifica se o horário está dentro do almoço
           horario = horario + timedelta(hours = 1) #se almoço, pula 1h
        
    return hr_disp
       
       
    #  count = 0
    #  for ag in qs:
    #   if ag.data_horario.date()==data and ag.data_horario.hour == horario.hour and ag.data_horario.minute == horario.minute: #verifica se existe algum agendamento no horário corrente da iteração
    #    count = count+1   
    #  if count == 0: #se não existir, popular lista de horários disponíveis
    #   hr = f"{data} {horario.hour}:{horario.minute}"
    #   hr = datetime.strptime(hr, "%Y-%m-%d %H:%M")
    #   hr_disp.append(hr)
      
    #  horario = horario + timedelta(minutes = 30)
    #  if horario.hour == 12: #verifica se o horário está dentro do almoço
    #    horario = horario + timedelta(hours = 1) #se almoço, pula 1h
       
   elif data.weekday() == 5: #verifica se é sábado
    horario_final = datetime(year=data.year, month=data.month, day = data.day, hour = 13, minute = 0, tzinfo=timezone.utc)
    while horario < horario_final:
        if not qs.filter(data_horario=horario).exists():
           hr_disp.append(horario)
        horario = horario + delta
    return hr_disp
      
    
   elif data.weekday() == 6: #verifica se é domingo
    raise serializers.ValidationError("Sem horários disponíveis no domingo")      
    
  
   return hr_disp    #retorna lista de horários disponíveis
 
 
