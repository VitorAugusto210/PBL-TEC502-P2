import requests
import threading
import random
import time

# --- Configuração do Teste ---
NUMERO_DE_REQUISICOES_SIMULTANEAS = 10  # Aumente para simular mais usuários

# URLs dos serviços de empresa expostos no localhost
URLS_EMPRESAS = [
    "http://localhost:8001",
    "http://localhost:8002",
    "http://localhost:8003",
]

# Carteiras de usuários para simulação
USER_ADDRESSES = [
    "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1",
    "0xFFcf8FDEE72ac11b5c542428B35EEF5769C409f0",
    "0x22d491Bde2303f2f43325b2108D26f1eAbA1e32b",
    "0xE11BA2b4D45Eaed5996Cd0823791E0C93114882d",
    "0xd03ea8624C8C5987235048901fB614fDcA89b117",
]

# --- Funções de Teste ---

def tentar_reservar(thread_id, url_empresa, user_address, station_id):
    """Função que cada thread executará para tentar fazer uma reserva."""
    print(f"[Thread {thread_id}] Tentando reservar estação {station_id} na {url_empresa}...")
    try:
        response = requests.post(
            f"{url_empresa}/reserva",
            json={"user_address": user_address, "station_id": station_id},
            timeout=20
        )
        if response.status_code == 200:
            print(f"✅ [Thread {thread_id}] SUCESSO! Reserva na estação {station_id} realizada. Session ID: {response.json().get('session_id')}")
        else:
            print(f"❌ [Thread {thread_id}] FALHA! Status: {response.status_code}, Resposta: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"🔥 [Thread {thread_id}] ERRO DE CONEXÃO: {e}")

# --- Cenários de Teste ---

def teste_1_reserva_dupla():
    """
    TESTE 1: Condição de Corrida no Smart Contract.
    Todos os usuários tentam reservar a MESMA estação ao mesmo tempo.
    Resultado esperado: Apenas UMA requisição terá sucesso. Todas as outras devem falhar
    com a mensagem "Estacao de recarga ja esta reservada."
    """
    print("\n--- INICIANDO TESTE 1: TENTATIVA DE RESERVA DUPLA ---")
    print(f"Disparando {NUMERO_DE_REQUISICOES_SIMULTANEAS} requisições para a MESMA estação (ID 777)...\n")
    
    threads = []
    ESTACAO_ID_CONCORRENTE = 777

    for i in range(NUMERO_DE_REQUISICOES_SIMULTANEAS):
        # Distribui as requisições aleatoriamente entre as empresas
        empresa_alvo = random.choice(URLS_EMPRESAS)
        user_alvo = random.choice(USER_ADDRESSES)
        
        thread = threading.Thread(target=tentar_reservar, args=(i + 1, empresa_alvo, user_alvo, ESTACAO_ID_CONCORRENTE))
        threads.append(thread)
        thread.start()
        time.sleep(0.05) # Pequeno delay para garantir que as threads iniciem quase juntas

    for thread in threads:
        thread.join()

    print("\n--- TESTE 1 CONCLUÍDO ---")


def teste_2_gerenciamento_de_nonce():
    """
    TESTE 2: Conflito de Nonce entre Serviços.
    Vários usuários fazem reservas em estações DIFERENTES ao mesmo tempo,
    usando todas as empresas.
    Resultado esperado: TODAS as requisições devem ter sucesso, pois cada empresa
    usa sua própria conta Ethereum e gerencia seu próprio nonce.
    """
    print("\n--- INICIANDO TESTE 2: GERENCIAMENTO DE NONCE ---")
    print(f"Disparando {NUMERO_DE_REQUISICOES_SIMULTANEAS} requisições para estações DIFERENTES...\n")
    
    threads = []

    for i in range(NUMERO_DE_REQUISICOES_SIMULTANEAS):
        empresa_alvo = random.choice(URLS_EMPRESAS)
        user_alvo = random.choice(USER_ADDRESSES)
        estacao_id_unica = 1000 + i  # Garante que cada estação é única

        thread = threading.Thread(target=tentar_reservar, args=(i + 1, empresa_alvo, user_alvo, estacao_id_unica))
        threads.append(thread)
        thread.start()
        time.sleep(0.05)

    for thread in threads:
        thread.join()

    print("\n--- TESTE 2 CONCLUÍDO ---")


if __name__ == "__main__":
    # Garanta que todos os seus contêineres (docker-compose up) estão rodando antes de executar este script.
    
    # --- Execute um teste de cada vez para analisar os resultados ---
    
    teste_1_reserva_dupla()
    
    print("\n" + "="*50 + "\n")
    
    # Descomente a linha abaixo para rodar o segundo teste
    #teste_2_gerenciamento_de_nonce()