from rest_framework import serializers
from datetime import datetime
from django.utils import timezone

from agenda.models import Agendamento


class AgendamentoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Agendamento
        fields = ['id', 'data_horario', 'nome_cliente', 'email_cliente', 'telefone_cliente', 'cancelamento_agendamento']
    
    
    def validate_data_horario(self, value):
        if value < timezone.now():
           raise serializers.ValidationError("Agendamento não pode ser feito no passado!")
       
        elif value.minute % 30 != 0:
           raise serializers.ValidationError("Horário inválido")
       
        elif value.weekday() == 6:
           raise serializers.ValidationError("Barbearia fechada aos domingos") 
        
        elif value.weekday()!=5 and (value.hour < 9 or value.hour > 17 or value.hour == 12) :
             raise serializers.ValidationError("Barbearia fechada para almoço")
         
        elif value.weekday()==5 and (value.hour < 9 or value.hour > 12):
             raise serializers.ValidationError("Barbearia fechada, sábado fecha às 13h")
            
        
        
        
       
       
        return value