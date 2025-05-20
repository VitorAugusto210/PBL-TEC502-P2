import random
import string
import time
import requests
from datetime import datetime
from gerar_rota import gerar_rota_autonoma, CAPITAIS_BRASIL  # importar sua base e função

def gerar_id_carro():
    return "carro_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))

def escolher_cidades():
    cidades = random.sample(CAPITAIS_BRASIL, 2)
    return cidades[0]["cidade"], cidades[1]["cidade"]

def simular_carro():
    carro_id = gerar_id_carro()
    origem, destino = escolher_cidades()

    print(f"\n🚗 {carro_id} vai de {origem} para {destino}")

    try:
        rota_json, empresa_origem = gerar_rota_autonoma(origem, destino, carro_id)
        url_rota = f"http://{empresa_origem}:8000/rota"
        response = requests.post(url_rota, json=rota_json)

        if response.status_code == 200:
            print(f"✅ [{carro_id}] Rota reservada com sucesso")
        else:
            print(f"❌ [{carro_id}] Falha na reserva: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"❌ [{carro_id}] Erro: {e}")

def loop_simulacao(tempo=10):
    while True:
        simular_carro()
        time.sleep(tempo)

if __name__ == "__main__":
    loop_simulacao(tempo=15)
