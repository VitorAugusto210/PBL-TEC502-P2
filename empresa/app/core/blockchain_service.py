# /empresa/app/core/blockchain_service.py

import json
import os
from web3 import Web3
from web3.middleware import geth_poa_middleware # Para redes PoA como Ganache
from hexbytes import HexBytes # Para lidar com o tx_hash de forma consistente

# --- Configurações Lidas de Variáveis de Ambiente ---
# Estas serão definidas no seu docker-compose.yml para cada serviço de empresa
BLOCKCHAIN_NODE_URL = os.getenv("GANACHE_URL", "http://localhost:8545")
# O endereco do contrato implantado. Sera diferente para cada deploy.
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
# Caminho para o arquivo JSON do ABI gerado pela compilacao do smart contract
ABI_FILE_PATH = os.getenv("ABI_FILE_PATH", "/app/blockchain_build/LedgerRecarga.json")
# A chave privada da conta Ethereum que esta empresa usara para assinar transacoes.
# CADA EMPRESA DEVE TER SUA PROPRIA CHAVE PRIVADA EM UM AMBIENTE REAL/SEGURO.
# Para desenvolvimento, pode ser uma das chaves fornecidas pelo Ganache.
COMPANY_ACCOUNT_PRIVATE_KEY = os.getenv("COMPANY_PRIVATE_KEY")


class BlockchainService:
    def __init__(self):
        if not BLOCKCHAIN_NODE_URL:
            raise ValueError("GANACHE_URL (URL do no blockchain) nao configurado.")
        if not CONTRACT_ADDRESS:
            raise ValueError("CONTRACT_ADDRESS (Endereco do Contrato) nao configurado.")
        if not ABI_FILE_PATH:
            raise ValueError("ABI_FILE_PATH (Caminho para o ABI do Contrato) nao configurado.")

        self.web3 = Web3(Web3.HTTPProvider(BLOCKCHAIN_NODE_URL))

        # Middleware para compatibilidade com redes Proof-of-Authority (PoA) como o Ganache
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        if not self.web3.is_connected():
            raise ConnectionError(
                f"Nao foi possivel conectar ao no blockchain em {BLOCKCHAIN_NODE_URL}"
            )

        self.contract_abi = self._load_abi()
        self.contract = self.web3.eth.contract(
            address=CONTRACT_ADDRESS, abi=self.contract_abi
        )

        if COMPANY_ACCOUNT_PRIVATE_KEY:
            self.account