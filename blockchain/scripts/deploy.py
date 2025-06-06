import json
import os
import time
from web3 import Web3, exceptions
from solcx import compile_standard, install_solc

def connect_to_blockchain(url, timeout=60):
    """Tenta conectar ao nó blockchain por um determinado período."""
    print(f"Tentando conectar a {url}...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            w3 = Web3(Web3.HTTPProvider(url))
            if w3.is_connected():
                print("Conectado ao blockchain com sucesso!")
                return w3
        except (exceptions.ConnectionError, exceptions.ExtraDataLengthError) as e:
            # Ignora erros de conexão temporários
            pass
        time.sleep(2)
    raise ConnectionError(f"Não foi possível conectar ao blockchain em {url} após {timeout} segundos.")

def main():
    """Função principal para compilar, fazer deploy e interagir com o contrato."""
    # Instala a versão correta do compilador Solidity
    try:
        install_solc('0.8.0')
    except Exception as e:
        print(f"Erro ao instalar o solc: {e}")
        # Tenta continuar, pode já estar instalado no ambiente

    # Conecta ao Ganache com tentativas
    provider_url = os.environ.get("BLOCKCHAIN_PROVIDER_URL", "http://ganache:8545")
    w3 = connect_to_blockchain(provider_url)

    # Define o endereço da conta que fará o deploy
    w3.eth.default_account = w3.eth.accounts[0]
    print(f"Usando a conta: {w3.eth.default_account}")

    # Compila o Smart Contract
    with open("./contracts/ChargePoint.sol", "r") as file:
        charge_point_file = file.read()

    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {"ChargePoint.sol": {"content": charge_point_file}},
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                    }
                }
            },
        },
        solc_version="0.8.0",
    )

    # Salva o ABI
    abi = compiled_sol["contracts"]["ChargePoint.sol"]["ChargePoint"]["abi"]
    with open("./scripts/abi.json", "w") as f:
        json.dump(abi, f)
    print("ABI salvo em scripts/abi.json")

    # Salva o bytecode
    bytecode = compiled_sol["contracts"]["ChargePoint.sol"]["ChargePoint"]["evm"]["bytecode"]["object"]
    with open("./scripts/bytecode.txt", "w") as f:
        f.write(bytecode)
    print("Bytecode salvo em scripts/bytecode.txt")

    # Deploy do contrato
    print("Fazendo deploy do contrato...")
    ChargePoint = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = ChargePoint.constructor().transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    print(f"Contrato 'ChargePoint' implantado no endereço: {tx_receipt.contractAddress}")

    # Salva o endereço do contrato
    with open("./scripts/contract_address.txt", "w") as f:
        f.write(tx_receipt.contractAddress)
    print("Endereço do contrato salvo em scripts/contract_address.txt")

if __name__ == "__main__":
    main()