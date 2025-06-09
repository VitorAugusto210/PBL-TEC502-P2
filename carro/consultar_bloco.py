import time 
from web3 import Web3

URL = "http://localhost:7545"

def consulta():
    w3 = Web3(Web3.HTTPProvider(URL, request_kwargs={'timeout': 5}))
    num_block = w3.eth.block_number
    print(f"Número do bloco: {num_block}") 
    time.sleep(0.5)


if __name__ == "__main__":
    while(1):
        consulta()
