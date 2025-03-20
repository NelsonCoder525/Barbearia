from django.contrib import admin
from django.urls import  path
from django.conf.urls import include
from agenda.views import  AgendamentoList, AgendamentoDetail, ClienteList,ClienteDetail, fidelizacoes_list, FidelidadeDetail, horarios_disponiveis, EnderecoList, healthcheck, create_user, relatorio_prestadores
from agenda.utils import get_horarios_list

urlpatterns = [
        path('agendamentos/', AgendamentoList.as_view()),    
        path('agendamentos/<int:pk>/', AgendamentoDetail.as_view()),    
        path('horarios/', horarios_disponiveis),
        path('prestadores/', relatorio_prestadores),
        path('clientes/', ClienteList.as_view()),
        path('clientes/<int:pk>/', ClienteDetail.as_view()),
        path('fidelidade/', fidelizacoes_list),
        path('fidelidade/<int:pk>/', FidelidadeDetail.as_view()),
        path('prestadores/<int:pk>/enderecos/', EnderecoList.as_view()),
        path('', healthcheck),
        path('register/', create_user, name='register'),
        
]