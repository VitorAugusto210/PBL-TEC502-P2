import json
import os
from web3 import Web3
import time
from web3.middleware import ExtraDataToPOAMiddleware
class BlockchainService:
    def __init__(self):
        self.provider_url = os.environ.get("BLOCKCHAIN_PROVIDER_URL", "http://ganache:8545")
        self.w3 = self._connect_with_retry()

        self.w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

        contract_address_path = "./blockchain/scripts/contract_address.txt"
        abi_path = "./blockchain/scripts/abi.json"
        
        self._wait_for_file(contract_address_path)
        with open(contract_address_path, 'r') as f:
            self.contract_address = f.read().strip()

        self._wait_for_file(abi_path)
        with open(abi_path, 'r') as f:
            self.abi = json.load(f)
            
        self.contract = self.w3.eth.contract(address=self.contract_address, abi=self.abi)
        self.w3.eth.default_account = self.w3.eth.accounts[0]
        print(f"BlockchainService inicializado. Conectado a {self.provider_url}, contrato em {self.contract_address}")

    def _connect_with_retry(self, timeout=60):
        print(f"Tentando conectar ao blockchain em {self.provider_url}...")
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                w3 = Web3(Web3.HTTPProvider(self.provider_url))
                if w3.is_connected():
                    print("Conexão com o blockchain estabelecida.")
                    return w3
            except Exception as e:
                print(f"Falha na conexão, tentando novamente... Erro: {e}")
            time.sleep(2)
        raise ConnectionError(f"Não foi possível conectar ao blockchain em {self.provider_url} após {timeout} segundos.")

    def _wait_for_file(self, filepath, timeout=30):
        start_time = time.time()
        while not os.path.exists(filepath):
            if time.time() - start_time > timeout:
                raise FileNotFoundError(f"Arquivo {filepath} não encontrado após {timeout} segundos.")
            time.sleep(1)

    def create_reservation(self, user_address: str, station_id: int):
        tx_hash = self.contract.functions.createReservation(
            Web3.to_checksum_address(user_address), 
            station_id
        ).transact({'from': self.w3.eth.default_account})
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        event = self.contract.events.ReservationCreated().process_receipt(receipt)
        session_id = event[0]['args']['sessionId']
        return session_id

    def finish_recharge(self, session_id: int, energy_consumed: int, cost: int):
        tx_hash = self.contract.functions.finishRecharge(
            session_id, 
            energy_consumed, 
            cost
        ).transact({'from': self.w3.eth.default_account})
        self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return True

    def make_payment(self, session_id: int, value_wei: int):
        tx_hash = self.contract.functions.makePayment(session_id).transact({
            'from': self.w3.eth.default_account,
            'value': value_wei
        })
        self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return True

    def get_session(self, session_id: int):
        return self.contract.functions.getSession(session_id).call()