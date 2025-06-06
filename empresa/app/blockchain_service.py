import json
import os
from web3 import Web3

class BlockchainService:
    def __init__(self):
        self.provider_url = os.environ.get("BLOCKCHAIN_PROVIDER_URL", "http://ganache:8545")
        self.w3 = Web3(Web3.HTTPProvider(self.provider_url))
        
        # Carrega o ABI e o endereço do contrato
        with open("./blockchain/scripts/abi.json", 'r') as f:
            self.abi = json.load(f)
        
        with open("./blockchain/scripts/contract_address.txt", 'r') as f:
            self.contract_address = f.read().strip()
            
        self.contract = self.w3.eth.contract(address=self.contract_address, abi=self.abi)
        self.w3.eth.default_account = self.w3.eth.accounts[0]

    def create_reservation(self, user_address: str, station_id: int):
        tx_hash = self.contract.functions.createReservation(
            Web3.to_checksum_address(user_address), 
            station_id
        ).transact()
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        # Recupera o ID da sessão a partir do evento
        event = self.contract.events.ReservationCreated().process_receipt(receipt)
        session_id = event[0]['args']['sessionId']
        return session_id

    def finish_recharge(self, session_id: int, energy_consumed: int, cost: int):
        tx_hash = self.contract.functions.finishRecharge(
            session_id, 
            energy_consumed, 
            cost
        ).transact()
        self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return True

    def make_payment(self, session_id: int, value_wei: int):
        tx_hash = self.contract.functions.makePayment(session_id).transact({'value': value_wei})
        self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return True

    def get_session(self, session_id: int):
        return self.contract.functions.getSession(session_id).call()

# Instância única para ser usada na aplicação
blockchain_service = BlockchainService()