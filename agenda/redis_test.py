import redis

# Conectando ao Redis no WSL
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Testando conexão
r.set("nome", "Corte de Cabelo Premium")
print(r.get("nome"))  # Deve imprimir "Corte de Cabelo Premium"
