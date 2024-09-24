import json, requests
from django.test import TestCase, Client
from rest_framework.test import APITestCase
from agenda.models import Agendamento
from datetime import datetime, timezone
from django.contrib.auth.models import User
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta, timezone, date

# Create your tests here.
class TestListagemAgendamentos(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='nelsonteste', password='test525')
        self.client = Client() 
        
    
    
    def test_listagem_vazia(self):
        self.client.login(username = "nelsonteste", password = "test525")
        response = self.client.get("http://127.0.0.1:8000/barber/agendamentos/?username=nelsonteste")
        data = response.json()
        self.assertEqual(data, [])
        
    def test_listagem_de_agendamentos_criados(self):
        User.objects.create(username = "Prestador Teste")
        prest = User.objects.first()
        Agendamento.objects.create(
        prestador = prest,
        data_horario=datetime(2024, 12, 15, 10, 30, 00, tzinfo=timezone.utc),
        nome_cliente="Cliente Teste",
        email_cliente="teste@gmail.com",
        telefone_cliente= "1334214343",
        estado_agendamento = "CO"
        )
       
        agendamento_serializado = {
        "id": 1,
        "data_horario" : "2024-12-15T10:30:00Z",
        "nome_cliente" : "Cliente Teste",
        "email_cliente" : "teste@gmail.com",
        "telefone_cliente" : "1334214343",
        "estado_agendamento" : "CO",
        "prestador": 1
         
       }
        
        self.client.login(username = "nelsonteste", password = "test525")
        response = self.client.get("http://127.0.0.1:8000/barber/agendamentos/?username=nelsonteste")
        data = response.json()
        self.assertDictEqual(data[0], agendamento_serializado)
        
class TestCriacaoAgendamento(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='nelsonteste', password='test525')
        self.client = Client() 
        self.client.login(username = "nelsonteste", password = "test525")
        
    def test_cria_agendamento(self):
        agendamento_request_data =  {
        "prestador": 1,
        "data_horario" : "2024-12-18 10:00:00",
        "nome_cliente" : "Cliente_Teste_estranho",
        "email_cliente" : "teste@gmail.com",
        "telefone_cliente" : "1334214343",
        "estado_agendamento" : "CO",
         
       }
        
        agendamento_serializado_2 = {
        "id": 1,
        "data_horario" : "2024-12-18T10:00:00Z",
        "nome_cliente" : "Cliente_Teste_estranho",
        "email_cliente" : "teste@gmail.com",
        "telefone_cliente" : "1334214343",
        "estado_agendamento" : "CO",
        "prestador": 1,
       }
        
        
        response_post = self.client.post("http://127.0.0.1:8000/barber/agendamentos/", agendamento_request_data, format = "json")
       
        
       
        response_get = self.client.get("http://127.0.0.1:8000/barber/agendamentos/?username=nelsonteste")
        data1 = response_get.json()
       
       
        
        self.assertEqual(data1[0], agendamento_serializado_2)
        
    def test_agendamento_detail_confirmar_agendamento_em_horario_ja_ocupado(self):
        prest = User.objects.first()
        Agendamento.objects.create(
        prestador = prest,    
        data_horario=datetime(2024, 12, 20, 15, 30, 00, tzinfo=timezone.utc),
        nome_cliente="Cliente Teste 3",
        email_cliente="teste3@gmail.com",
        telefone_cliente= "1334214343",
        estado_agendamento = "CO"
        )
        
        agendamento_request_data =  {
        "prestador": 1,
        "data_horario" : "2024-12-20 15:30:00",
        "nome_cliente" : "Outro Cliente",
        "email_cliente" : "oc@gmail.com",
        "telefone_cliente" : "1334214343",
        "estado_agendamento" : "CO",
         
       }
        
        response_post = self.client.post("http://127.0.0.1:8000/barber/agendamentos/", agendamento_request_data, format = "json")
        data = response_post.json()
                
        self.assertEqual(data, {'non_field_errors': ['Horário já ocupado']}) 
    
    def test_agendamento_no_domingo(self):
        agendamento_request_data =  {
        "prestador": 1,
        "data_horario" : "2024-09-29 15:30:00",
        "nome_cliente" : "Outro Cliente",
        "email_cliente" : "oc@gmail.com",
        "telefone_cliente" : "1334214343",
        "estado_agendamento" : "CO",
         
       }
            
        response_post = self.client.post("http://127.0.0.1:8000/barber/agendamentos/", agendamento_request_data, format = "json")
        data = response_post.json()
                
        self.assertEqual(data, {'data_horario': ['Barbearia fechada aos domingos']}) 
        
    
        
class TestAgendamentoDetail(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='nelsonteste', password='test525', is_superuser = True)
        self.client = Client() 
        self.client.login(username = "nelsonteste", password = "test525")
        
    def test_agendamento_detail_get(self):
        
        presta = User.objects.first()
        
        Agendamento.objects.create(
        prestador = presta,
        data_horario=datetime(2024, 12, 15, 9, 30, 00, tzinfo=timezone.utc),
        nome_cliente="Cliente Teste 2",
        email_cliente="teste@gmail.com",
        telefone_cliente= "1334214343",
        estado_agendamento = "CO"
        )
        
        
        response_get_2 = self.client.get("http://127.0.0.1:8000/barber/agendamentos/?username=nelsonteste")
        data = response_get_2.json()
        
        
        agendamento_serializado_3 = {
        "id": 1,
        "data_horario" : "2024-12-15T09:30:00Z",
        "nome_cliente" : "Cliente Teste 2",
        "email_cliente" : "teste@gmail.com",
        "telefone_cliente" : "1334214343",
        "estado_agendamento": "CO",
        "prestador": 1
         
       }
        
        self.assertEqual(data[0], agendamento_serializado_3)
        
        
    def test_agendamento_detail_patch(self):
        
        prest = User.objects.first()
        Agendamento.objects.create(
        prestador = prest,    
        data_horario=datetime(2024, 12, 20, 15, 30, 00, tzinfo=timezone.utc),
        nome_cliente="Cliente Teste 3",
        email_cliente="teste3@gmail.com",
        telefone_cliente= "1334214343",
        estado_agendamento = "CO"
        )
        
        
        agendamento_request_data1 =  {
        
        "data_horario" : "2024-10-25T16:30:00Z",
        "nome_cliente" : "NELSON RIBEIRO",
        "email_cliente" : "nelsonr525@gmail.com",
        "telefone_cliente" : "1334214343",
         
       }
        
        agendamento_serializado_4 = {
        "id": 1,
        "data_horario" : "2024-10-25T16:30:00Z",
        "nome_cliente" : "NELSON RIBEIRO",
        "email_cliente" : "nelsonr525@gmail.com",
        "telefone_cliente" : "1334214343",
        "estado_agendamento": "CO",
        "prestador": 1
        
       }
        response_patch = self.client.patch("http://127.0.0.1:8000/barber/agendamentos/1/", agendamento_request_data1, content_type="application/json")
        
       
        response_get3 = self.client.get("http://127.0.0.1:8000/barber/agendamentos/?username=nelsonteste")
        data3 = response_get3.json()
        
        
        
        self.assertEqual(data3[0], agendamento_serializado_4)
    
    def test_agendamento_no_domingo_patch(self):
        
        prest = User.objects.first()
        Agendamento.objects.create(
        prestador = prest,    
        data_horario=datetime(2024, 12, 20, 15, 30, 00, tzinfo=timezone.utc),
        nome_cliente="Cliente Teste 3",
        email_cliente="teste3@gmail.com",
        telefone_cliente= "1334214343",
        estado_agendamento = "CO"
        )
        
        
        agendamento_request_data1 =  {
        
        "data_horario" : "2024-09-29T16:30:00Z",
        
         
       }
        
    
        
       
        response_patch = self.client.patch("http://127.0.0.1:8000/barber/agendamentos/1/", agendamento_request_data1, content_type="application/json")
        data = response_patch.json()
        
        
        
        self.assertEqual(data, {'data_horario': ['Barbearia fechada aos domingos']})
        
             
        
        
        
        
        
        
    def test_agendamento_detail_delete(self):
       
       prest = User.objects.first()
       
       Agendamento.objects.create(
        prestador = prest,
        data_horario=datetime(2024, 12, 20, 15, 30, 00, tzinfo=timezone.utc),
        nome_cliente="Cliente Teste 1000",
        email_cliente="teste3@gmail.com",
        telefone_cliente= "1334214343",
        estado_agendamento = "AG",
        
        )
       
       response = self.client.delete("/api/agendamentos/1/")
       response_get = self.client.get("http://127.0.0.1:8000/barber/agendamentos/?username=nelsonteste")
       data = response_get.json()
   
       self.assertEqual(data, [])