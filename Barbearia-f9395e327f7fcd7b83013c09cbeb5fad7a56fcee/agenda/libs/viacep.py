from datetime import date
from django.conf import settings
import logging
import requests
from rest_framework import serializers

@staticmethod
def endereco(cep: str):
  
  logging.info(f"Fazendo requisição para BrasilAPI para o CEP: {cep}")
  if settings.TESTING == True:
    logging.info("Requisição não está sendo feita pois TESTING = True")
    if cep == 11747116:
      
      return {'cep': "11747116",
              'uf': "São Paulo",
              'localidade': "Itanhaém",
              'bairro': "Sabaúna", 
              'logradouro': "Rua Professor Luiz Carlos de Souza",
              'complemento': ""      

      }
    else: 
        return ""  

 
  r = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
  if r.status_code != 200:
    logging.error("Algum erro ocorreu na viacep")
    raise serializers.ValidationError(f"Errinho {r.status_code}")

  endereco = r.json()
  return endereco


  
  