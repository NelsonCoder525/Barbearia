import csv
from io import StringIO
from django.contrib.auth.models import User
from agenda.serializers import PrestadorSerializer
from celery import Celery
from barbearia.celery import app
from django.core.mail import EmailMessage

@app.task
def gera_relatorio_prestadores():
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Prestador", "Data e Horario", "E-mail Cliente", "Telefone Cliente", "Estado do Agendamento"])
    
    prestadores = User.objects.all()
    serializer = PrestadorSerializer(prestadores, many=True)
    
    for prestador in serializer.data:
        for agendamento in prestador["agendamentos"]:
            writer.writerow([
                agendamento["prestador"], 
                agendamento["data_horario"],
                agendamento["email_cliente"],
                agendamento["telefone_cliente"],
                agendamento["estado_agendamento"]
            ])
    email = EmailMessage(
        'Relatório de Prestadores',
        'Segue em anexo o relatório de prestadores',
        'nelsonrqj@gmail.com',
        ['nelsonrqj@gmail.com']
    )
        
        
    email.attach("relatorio.csv", output.getvalue(), "text/csv")
    email.send()
    return output.getvalue()
    #print(output.getvalue())
    