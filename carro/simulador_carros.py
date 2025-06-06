import requests
import time
import random

EMPRESA_API_URL = "http://empresa:8000"

def consultar_rota(carro_id, localizacao_atual, localizacao_destino):
    """Consulta a API da empresa para obter uma rota."""
    try:
        response = requests.post(f"{EMPRESA_API_URL}/gerar_rota", json={
            "localizacao_atual": localizacao_atual,
            "localizacao_destino": localizacao_destino
        })
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Carro {carro_id}: Erro ao consultar rota: {e}")
        return None

def fazer_reserva(user_address, station_id):
    """Faz a reserva de um ponto de recarga."""
    try:
        response = requests.post(f"{EMPRESA_API_URL}/reserva", json={
            "user_address": user_address,
            "station_id": station_id
        })
        response.raise_for_status()
        print(f"Reserva para {user_address} no posto {station_id} realizada com sucesso.")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer reserva: {e}")
        return None

def finalizar_recarga(session_id, energy, cost):
    """Informa a finalização da recarga."""
    try:
        response = requests.post(f"{EMPRESA_API_URL}/finalizar-recarga", json={
            "session_id": session_id,
            "energy_consumed": energy,
            "cost": cost
        })
        response.raise_for_status()
        print(f"Sessão {session_id}: Recarga finalizada com {energy}Wh ao custo de {cost} Wei.")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao finalizar recarga: {e}")
        return None

def fazer_pagamento(session_id, cost):
    """Realiza o pagamento da recarga."""
    try:
        response = requests.post(f"{EMPRESA_API_URL}/pagamento", json={
            "session_id": session_id,
            "value": cost
        })
        response.raise_for_status()
        print(f"Sessão {session_id}: Pagamento de {cost} Wei realizado.")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao realizar pagamento: {e}")
        return None


def simular_carro(carro_id):
    """Simula o comportamento de um carro."""
    # Endereços de exemplo do Ganache
    user_addresses = [
        "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1",
        "0xFFcf8FDEE72ac11b5c542428B35EEF5769C409f0",
        "0x22d491Bde2303f2f43325b2108D26f1eAbA1e32b"
    ]
    
    user_address = random.choice(user_addresses)
    localizacao_atual = {"latitude": -12.255, "longitude": -38.955}
    localizacao_destino = {"latitude": -12.26, "longitude": -38.95} # Posto de gasolina
    station_id = random.randint(1, 100)
    
    print(f"Carro {carro_id} (Usuário: {user_address[:10]}...) iniciando simulação...")

    # 1. Fazer reserva
    reserva_info = fazer_reserva(user_address, station_id)
    if not reserva_info or "session_id" not in reserva_info:
        print(f"Carro {carro_id}: Falha ao obter ID da sessão. Abortando.")
        return
        
    session_id = reserva_info["session_id"]
    print(f"Carro {carro_id}: Reserva confirmada. ID da Sessão: {session_id}")
    
    # 2. Obter rota
    rota_info = consultar_rota(carro_id, localizacao_atual, localizacao_destino)
    if not rota_info:
        return

    print(f"Carro {carro_id}: Rota recebida: {rota_info['rota']}")
    time.sleep(2) # Simula o tempo de viagem

    print(f"Carro {carro_id}: Chegou ao destino e iniciou a recarga.")
    time.sleep(5) # Simula o tempo de recarga

    # 3. Finalizar recarga e pagar
    energia_consumida = random.randint(1000, 5000) # Em Wh
    custo_wei = energia_consumida * 100 # Custo simbólico em Wei
    
    finalizar_recarga(session_id, energia_consumida, custo_wei)
    fazer_pagamento(session_id, custo_wei)

    print(f"Carro {carro_id}: Simulação concluída.")

if __name__ == "__main__":
    time.sleep(15) # Espera o deploy do contrato e a API subir
    print("Iniciando simulação dos carros...")
    simular_carro(1)