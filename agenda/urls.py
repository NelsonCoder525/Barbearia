from django.contrib import admin
from django.urls import  path
from django.conf.urls import include
from agenda.views import horarios_list, AgendamentoList, AgendamentoDetail, PrestadorList, ClienteList,ClienteDetail, fidelizacoes_list, FidelidadeDetail
urlpatterns = [
        path('agendamentos/', AgendamentoList.as_view()),    
        path('agendamentos/<int:pk>/', AgendamentoDetail.as_view()),    
        path('horarios/', horarios_list),
        path('prestadores/', PrestadorList.as_view()),
        path('clientes/', ClienteList.as_view()),
        path('clientes/<int:pk>/', ClienteDetail.as_view()),
        path('fidelidade/', fidelizacoes_list),
        path('fidelidade/<int:pk>/', FidelidadeDetail.as_view())
]