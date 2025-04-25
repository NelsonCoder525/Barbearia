from datetime import date
from django.conf import settings
import logging
import requests




def is_feriado(date: date) -> bool:
  logging.info(f"Fazendo requisição para BrasilAPI para a data: {date.isoformat()}")
  if settings.TESTING == True:
    logging.info("Requisição não está sendo feita pois TESTING = True")
    if date.day == 25 and date.month == 12:
      
      return True
   
    return False
  ano = date.year
  r = requests.get(f"https://brasilapi.com.br/api/feriados/v1/{ano}")
  
  if r.status_code != 200:
    logging.error("Algum erro ocorreu na Brasil API")
    return False
    #raise ValueError("Não foi possível consultar os feriados!")
  
  feriados = r.json()
  for feriado in feriados:
    data_feriado_as_str = feriado["date"]
    data_feriado = date.fromisoformat(data_feriado_as_str)
    if date == data_feriado:
      return True
  return False

