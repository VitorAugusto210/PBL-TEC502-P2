import json
import os
from web3 import Web3
from web3.exceptions import ContractLogicError
from datetime import datetime


GANACHE_URL = "http://localhost:7545"

ABI_PATH = "./blockchain/scripts/abi.json"
ADDRESS_PATH = "./blockchain/scripts/contract_address.txt"

def listar_reservas():
    """
    Conecta ao blockchain, carrega o contrato e lista todas as
    reservas registradas de forma legível.
    """
    # --- 1. Conectar ao Ganache ---
    print(f"Tentando conectar ao Ganache em: {GANACHE_URL}")
    try:
        w3 = Web3(Web3.HTTPProvider(GANACHE_URL, request_kwargs={'timeout': 5}))
        if not w3.is_connected():
            print("\nERRO: Falha ao conectar. Verifique se os seus contêineres estão rodando com 'docker-compose up'.")
            return
    
    except Exception as e:
        print(f"\nOcorreu um erro inesperado durante a conexão: {e}")
        return

    print("✅ Conexão com o Ganache bem-sucedida.")

    # --- 2. Carregar o Contrato ---
    try:
        with open(ADDRESS_PATH, 'r') as f:
            contract_address = f.read().strip()
        with open(ABI_PATH, 'r') as f:
            contract_abi = json.load(f)
    except FileNotFoundError as e:
        print(f"\nERRO: Arquivo de contrato não encontrado: {e}")
        print("Certifique-se de que o serviço 'blockchain_deployer' foi executado com sucesso pelo menos uma vez.")
        return

    contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    print(f"Contrato carregado do endereço: {contract_address}")

    # --- 3. Listar as Reservas ---
    try:
        # Pega o ID da próxima sessão para saber até onde iterar.
        next_session_id = contract.functions.nextSessionId().call()
        
        print("\n=============================================")
        print("  HISTÓRICO DE TRANSAÇÕES NO BLOCKCHAIN  ")
        print("=============================================")

        if next_session_id == 1:
            print("Nenhuma reserva encontrada no ledger.")
            return

        # Itera de 1 até o último ID de sessão criado.
        for session_id in range(1, next_session_id):
            try:
                # Chama a função 'getSession' do smart contract para obter os dados.
                session_data = contract.functions.getSession(session_id).call()
                
                # Formata os dados para exibição
                user, station_id, start_time, end_time, energy, cost, is_paid = session_data
                
                print(f"\n[ SESSÃO ID: {session_id} ]")
                print(f"  - Usuário: {user}")
                print(f"  - Estação: {station_id}")
                print(f"  - Início: {datetime.fromtimestamp(start_time).strftime('%d/%m/%Y %H:%M:%S')}")
                if end_time > 0:
                    print(f"  - Fim: {datetime.fromtimestamp(end_time).strftime('%d/%m/%Y %H:%M:%S')}")
                else:
                    print("  - Fim: Recarga em andamento")
                print(f"  - Consumo: {energy} Wh")
                print(f"  - Custo: {w3.from_wei(cost, 'ether')} ETH") # Converte de Wei para Ether
                print(f"  - Status: {'Pago' if is_paid else 'Aguardando Pagamento'}")

            except ContractLogicError:
                # Ocorre se a sessão foi cancelada e o 'require(session.exists...)' falhou.
                print(f"\n[ SESSÃO ID: {session_id} ] - CANCELADA ou INVÁLIDA.")

    except Exception as e:
        print(f"\nOcorreu um erro ao buscar as reservas: {e}")

if __name__ == "__main__":
    listar_reservas()