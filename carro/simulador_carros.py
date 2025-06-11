import requests
import time
import random
import os

EMPRESAS = {
    "empresa_a": os.getenv("EMPRESA_A_URL", "http://localhost:8001"),
    "empresa_b": os.getenv("EMPRESA_B_URL", "http://localhost:8002"),
    "empresa_c": os.getenv("EMPRESA_C_URL", "http://localhost:8003"),
}

NOME_EMPRESA, EMPRESA_API_URL = random.choice(list(EMPRESAS.items()))


def fazer_reserva(user_address, station_id):
    """Faz a reserva de um ponto de recarga."""
    print(f"Tentando fazer reserva em {EMPRESA_API_URL}/reserva...")
    try:
        response = requests.post(f"{EMPRESA_API_URL}/reserva", json={
            "user_address": user_address,
            "station_id": station_id
        }, timeout=10)
        response.raise_for_status()
        print(f"Reserva para {user_address} na {NOME_EMPRESA} (posto {station_id}) realizada com sucesso.")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer reserva: {e}")
        return None

def finalizar_recarga(session_id, energy, cost):
    """Informa a finalização da recarga."""
    print(f"Finalizando recarga para sessão {session_id} em {EMPRESA_API_URL}/finalizar-recarga...")
    try:
        response = requests.post(f"{EMPRESA_API_URL}/finalizar-recarga", json={
            "session_id": session_id,
            "energy_consumed": energy,
            "cost": cost
        }, timeout=10)
        response.raise_for_status()
        print(f"Sessão {session_id}: Recarga finalizada com {energy}Wh ao custo de {cost} Wei.")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao finalizar recarga: {e}")
        return None

def fazer_pagamento(session_id, cost):
    """Realiza o pagamento da recarga."""
    print(f"Realizando pagamento para sessão {session_id} em {EMPRESA_API_URL}/pagamento...")
    try:
        response = requests.post(f"{EMPRESA_API_URL}/pagamento", json={
            "session_id": session_id,
            "value": cost
        }, timeout=10)
        response.raise_for_status()
        print(f"Sessão {session_id}: Pagamento de {cost} Wei realizado.")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao realizar pagamento: {e}")
        return None


def simular_carro(carro_id):
    """Simula o comportamento de um carro."""
    user_addresses = [
        "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1",
        "0xFFcf8FDEE72ac11b5c542428B35EEF5769C409f0",
        "0x22d491Bde2303f2f43325b2108D26f1eAbA1e32b"
    ]
    
    user_address = random.choice(user_addresses)
    station_id = random.randint(1, 100)
    
    print(f"Carro {carro_id} (Usuário: {user_address[:10]}...) iniciando simulação na empresa '{NOME_EMPRESA}'...")


    reserva_info = fazer_reserva(user_address, station_id)
    if not reserva_info or "session_id" not in reserva_info:
        print(f"Carro {carro_id}: Falha ao obter ID da sessão. Abortando.")
        return
        
    session_id = reserva_info["session_id"]
    print(f"Carro {carro_id}: Reserva confirmada. ID da Sessão: {session_id}")
    
    # Simula tempo de viagem e recarga
    print(f"Carro {carro_id}: Viajando para o posto de recarga...")
    time.sleep(3)
    print(f"Carro {carro_id}: Chegou ao destino e iniciou a recarga.")
    time.sleep(5)

    # 3. Finalizar recarga e pagar
    energia_consumida = random.randint(1000, 5000)
    custo_wei = energia_consumida * 100 
    
    finalizar_recarga(session_id, energia_consumida, custo_wei)
    time.sleep(1)
    fazer_pagamento(session_id, custo_wei)

    print(f"\n--- Simulação para Carro {carro_id} concluída com sucesso! ---\n")

if __name__ == "__main__":
    print("Iniciando simulação dos carros...")
    
    # Simula 3 carros para testar
    for i in range(3):
        simular_carro(i + 1)
        time.sleep(2)