from django.db import models

class Agendamento(models.Model):
    prestador = models.ForeignKey('auth.User', related_name="agendamentos", on_delete = models.CASCADE)
    
    data_horario = models.DateTimeField()
    nome_cliente = models.CharField(max_length=200)
    email_cliente = models.EmailField()
    telefone_cliente = models.CharField(max_length=20)
        
    agendado = 'AG'
    confirmado = 'CO'
    cancelado = 'CA'
    executado = 'EX'
    
    ESTADOS_AGENDAMENTO_CHOICES = [
        (agendado, 'agendado'),
        (confirmado, 'confirmado'),
        (cancelado, 'cancelado'),
        (executado, 'executado')       
    ]

    estado_agendamento = models.CharField(max_length=2, choices=ESTADOS_AGENDAMENTO_CHOICES, default=agendado)
    
    def get_agendamentos_confirmados(self):
        todos_agendamentos_confirmados = Agendamento.objects.filter(estado_agendamento = 'CO')
        return todos_agendamentos_confirmados

class Cliente(models.Model):
    nome = models.CharField(max_length=200)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    
class Fidelidade(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete = models.CASCADE)
    prestador_fidelidade = models.ForeignKey('auth.User', related_name="agendamentos_fidelidade", on_delete = models.CASCADE)
    agendamento_id = models.ForeignKey(Agendamento, on_delete = models.CASCADE)
    