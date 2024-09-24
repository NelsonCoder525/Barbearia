from rest_framework import serializers
from django.utils import timezone
from datetime import datetime, timedelta, time, date
from agenda.models import Agendamento, Cliente, Fidelidade
from django.contrib.auth.models import User


class AgendamentoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Agendamento
        fields = '__all__'
    
    
    def validate_data_horario(self, value):
        if value < timezone.now():
           raise serializers.ValidationError("Agendamento não pode ser feito no passado!")
       
        elif value.minute % 30 != 0: #só permite que horários sejam cadastrados com minutos iguais  00 ou 30
           raise serializers.ValidationError("Horário inválido")
       
        elif value.weekday() == 6:
           raise serializers.ValidationError("Barbearia fechada aos domingos") 
        
        elif value.weekday()!=5 and (value.hour < 9 or value.hour > 17 or value.hour == 12) :
             raise serializers.ValidationError("Barbearia fechada")
         
        elif value.weekday()==5 and (value.hour < 9 or value.hour > 12):
             raise serializers.ValidationError("Barbearia fechada, sábado fecha às 13h")
            
        
        
        
       
       
        return value
     
     
    def validate(self, request):
        telefone_cliente = request.get("telefone_cliente", "")
        email_cliente = request.get("email_cliente", "")
        dt = request.get("data_horario", "")
        prestador_cliente = request.get("prestador", "")
        estado_agendamento_request = request.get("estado_agendamento", "")
        
         
        req = self.context.get('request')
        
        if request and req.method == 'POST':
           #VALIDAÇÃO DO TELEFONE 
           tel = list(telefone_cliente)  
        
           for x in tel:
              if x.isnumeric() == False and x !="(" and x !=")" and x !="+" and x!="-":
               print(x)
               raise serializers.ValidationError("Telefone só deve conter dígitos, hífen, parênteses ou '+'")
           if "+" in tel and tel.index("+")!=0:
             raise serializers.ValidationError("'+' só no início")
                   
           elif len(telefone_cliente) < 8:
             raise serializers.ValidationError("Telefone deve ter no mínimo 8 dígitos")
       
           elif email_cliente.endswith(".br") and telefone_cliente.startswith("+") and not telefone_cliente.startswith("+55"):
             raise serializers.ValidationError("E-mail brasileiro deve estar associado a um número do Brasil (+55)")
           
           
           agendamentos_cliente = Agendamento.objects.filter(email_cliente = email_cliente, estado_agendamento = 'CO')#TRAZ TODOS AGENDAMENTOS CONFIRMADOS CADASTRADOS COM O E-MAIL INFORMADO NA REQUISIÇÃO 
           #VALIDAÇÃO DE APENAS UM AGENDAMENTO POR DIA PARA O MESMO E-MAIL     
           for agendamento in agendamentos_cliente:
             if dt != "":            
                if agendamento.data_horario.date() == dt.date():
                  raise serializers.ValidationError("Apenas um agendamento por dia")
        
           todos_agendamentos = Agendamento.objects.filter(estado_agendamento = 'CO')#TRAZ TODOS AGENDAMENTOS CONFIRMADOS
           #VALIDAÇÃO DE HORÁRIO JÁ OCUPADO
           for agendamento in todos_agendamentos:
              if dt == agendamento.data_horario:
               raise serializers.ValidationError("Horário já ocupado")
            
           
           
        #SE FOR REQUISIÇÃO DO MODO PATCH(MODIFICAÇÃO)    
        if request and req.method == 'PATCH':
           instance = self.instance
           id = instance.id #TRAZ O ID DO AGENDAMENTO QUE ESTOU MODIFICANDO
          
           
           agendamentos_cliente = Agendamento.objects.filter(email_cliente = instance.email_cliente, estado_agendamento = 'CO')  #TRAZ TODOS AGENDAMENTOS CONFIRMADOS COM O E-MAIL INFORMADO NA REQUISIÇÃO 
           #VALIDAÇÃO DE APENAS UM AGENDAMENTO POR DIA PARA O MESMO E-MAIL
           for agendamento in agendamentos_cliente: 
             if dt != "":           
                if agendamento.data_horario.date() == dt.date() and  id != agendamento.pk and estado_agendamento_request != 'AG' and estado_agendamento_request != 'CA' and estado_agendamento_request != "":
                  raise serializers.ValidationError("Apenas um agendamento por dia")
             else:
               dt_instance = instance.data_horario
               if agendamento.data_horario.date() == dt_instance.date() and  id != agendamento.pk and estado_agendamento_request != 'AG' and estado_agendamento_request != 'CA' and estado_agendamento_request != "":
                  raise serializers.ValidationError("Apenas um agendamento por dia")
           
           todos_agendamentos = Agendamento.objects.filter(estado_agendamento = 'CO')#TRAZ TODOS AGENDAMENTOS CONFIRMADOS
           #VALIDAÇÃO DE HORÁRIO JÁ OCUPADO
           for agendamento in todos_agendamentos:
              if dt != "": 
                 
                 if dt == agendamento.data_horario and id != agendamento.pk and estado_agendamento_request != 'AG' and estado_agendamento_request != 'CA' and estado_agendamento_request != "":
                 
                    raise serializers.ValidationError("Horário já ocupado")
              else:
                  dt_instance = instance.data_horario
                  if dt_instance == agendamento.data_horario and id != agendamento.pk and estado_agendamento_request != 'AG' and estado_agendamento_request != 'CA' and estado_agendamento_request != "":
                     raise serializers.ValidationError("Horário já ocupado")
           
           
           if telefone_cliente != "": #CONDICIONAL PARA CASO O TELEFONE ESTEJA SENDO MODIFICADO
            #VALIDAÇÃO DO TELEFONE          
            tel = list(telefone_cliente)  
            for x in tel:
              
             if x.isnumeric() == False and x !="(" and x !=")" and x !="+" and x!="-":
               print(x)
               raise serializers.ValidationError("Telefone só deve conter dígitos, hífen, parênteses ou '+'")
             
             elif "+" in tel and tel.index("+")!=0:
              raise serializers.ValidationError("'+' só no início")
                   
             elif len(telefone_cliente) < 8:
              raise serializers.ValidationError("Telefone deve ter no mínimo 8 dígitos")
       
             elif email_cliente.endswith(".br") and telefone_cliente.startswith("+") and not telefone_cliente.startswith("+55"):
              raise serializers.ValidationError("E-mail brasileiro deve estar associado a um número do Brasil (+55)") 
       
        
        
        return request    

class PrestadorSerializer(serializers.ModelSerializer):
      class Meta:
        model = User    
        fields = ['id', 'username', 'agendamentos']
      
      agendamentos = AgendamentoSerializer(many=True, read_only=True)      

class ClienteSerializer(serializers.ModelSerializer):
  class Meta:
    model = Cliente
    fields = '__all__'
    
  def validate(self, request):
        telefone = request.get("telefone", "")
        email = request.get("email", "")
        
        req = self.context.get('request')
        
        if request and req.method == 'POST':
           #VALIDAÇÃO DO TELEFONE 
           tel = list(telefone)  
        
           for x in tel:
              if x.isnumeric() == False and x !="(" and x !=")" and x !="+" and x!="-":
               print(x)
               raise serializers.ValidationError("Telefone só deve conter dígitos, hífen, parênteses ou '+'")
           if "+" in tel and tel.index("+")!=0:
             raise serializers.ValidationError("'+' só no início")
                   
           elif len(telefone) < 8:
             raise serializers.ValidationError("Telefone deve ter no mínimo 8 dígitos")
       
           elif email.endswith(".br") and telefone.startswith("+") and not telefone.startswith("+55"):
             raise serializers.ValidationError("E-mail brasileiro deve estar associado a um número do Brasil (+55)")
           
           
        if request and req.method == 'PATCH':   
          if telefone != "": #CONDICIONAL PARA CASO O TELEFONE ESTEJA SENDO MODIFICADO
            #VALIDAÇÃO DO TELEFONE          
            tel = list(telefone)  
            for x in tel:
              
             if x.isnumeric() == False and x !="(" and x !=")" and x !="+" and x!="-":
               print(x)
               raise serializers.ValidationError("Telefone só deve conter dígitos, hífen, parênteses ou '+'")
             
             elif "+" in tel and tel.index("+")!=0:
              raise serializers.ValidationError("'+' só no início")
                   
             elif len(telefone) < 8:
              raise serializers.ValidationError("Telefone deve ter no mínimo 8 dígitos")
       
             elif email.endswith(".br") and telefone.startswith("+") and not telefone.startswith("+55"):
              raise serializers.ValidationError("E-mail brasileiro deve estar associado a um número do Brasil (+55)") 
        
           
        return request
  
       
      
class FidelidadeSerializer(serializers.ModelSerializer):
     class Meta:
       model = Fidelidade
       fields = '__all__'
       
    
        
