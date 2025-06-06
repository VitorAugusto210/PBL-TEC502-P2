import json
from web3 import Web3
from datetime import datetime, timezone

# ======== CONFIGURAÇÃO DE CONEXÃO ========

def conectar_ganache():
    ganache_url = "http://127.0.0.1:7545"  # ajuste se necessário
    web3 = Web3(Web3.HTTPProvider(ganache_url))

    if not web3.is_connected():
        raise ConnectionError("Não foi possível conectar ao Ganache.")

    print("Conectado ao Ganache com sucesso!")
    web3.eth.default_account = web3.eth.accounts[0]
    print(f"Conta padrão: {web3.eth.default_account}")

    return web3

# ======== UTILITÁRIOS DE ARQUIVO ========

def carregar_abi(path='abi.json'):
    with open(path, 'r') as f:
        return json.load(f)

def carregar_bytecode(path='bytecode.txt'):
    with open(path, 'r') as f:
        return f.read().strip()

# ======== OPERAÇÕES COM CONTRATO ========

def implantar_contrato(web3, abi, bytecode):
    Contrato = web3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = Contrato.constructor().transact()
    print(f"Transação enviada, hash: {tx_hash.hex()}")
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Contrato implantado em: {tx_receipt.contractAddress}")
    return web3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

def registrar_reserva(contrato, carroId, pontoId, empresaId, janelaInicio, janelaFim):
    tx_hash = contrato.functions.registrarReserva(
        carroId, pontoId, empresaId, janelaInicio, janelaFim
    ).transact()
    tx_receipt = contrato.web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Reserva registrada com hash: {tx_receipt.transactionHash.hex()}")
    return tx_receipt

def consultar_reserva(contrato, id_reserva):
    return contrato.functions.getReserva(id_reserva).call()

# ======== PROGRAMA PRINCIPAL ========

def main():
    web3 = conectar_ganache()
    abi = carregar_abi()
    bytecode = carregar_bytecode()
    contrato = implantar_contrato(web3, abi, bytecode)

    # Exemplo: registrando uma reserva
    agora = int(datetime.now(timezone.utc).timestamp())
    daqui_uma_hora = agora + 3600

    registrar_reserva(contrato, "Carro123", "PontoA", "EmpresaX", agora, daqui_uma_hora)

    # Consultar a reserva
    reserva = consultar_reserva(contrato, 0)
    print("Reserva consultada:", reserva)

if __name__ == "__main__":
    main()
