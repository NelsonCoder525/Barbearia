from django.contrib import admin
from agenda.models import Agendamento, Cliente, Fidelidade, Endereco

# Register your models here.
admin.site.register(Agendamento)
admin.site.register(Cliente)
admin.site.register(Fidelidade)
admin.site.register(Endereco)