from django.contrib import admin
from django.urls import  path
from django.conf.urls import include
from agenda.views import agendamento_detail
from agenda.views import agendamento_list, horarios_list


urlpatterns = [
        path('agendamentos/', agendamento_list),    
        path('agendamentos/<int:id>/', agendamento_detail),    
        path('horarios/', horarios_list)
]