from web3 import Web3
import random
import time

w3 = Web3(Web3.HTTPProvider("http://localhost:7545"))

user_addresses = [
    "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1",
    "0xFFcf8FDEE72ac11b5c542428B35EEF5769C409f0",
    "0x22d491Bde2303f2f43325b2108D26f1eAbA1e32b"
]

INTERVALO_SEGUNDOS = 5 

while True:
    user = random.choice(user_addresses)
    saldo_antes = w3.eth.get_balance(user)
    custo_wei = w3.to_wei(random.uniform(0.001, 0.01), 'ether')
    saldo_depois = saldo_antes - custo_wei

    print("-" * 60)
    print(f"Usuário: {user}")
    print(f"Saldo antes da recarga: {w3.from_wei(saldo_antes, 'ether')} ETH")
    print(f"Valor pago na recarga: {w3.from_wei(custo_wei, 'ether')} ETH")
    print(f"Saldo após a recarga: {w3.from_wei(saldo_depois, 'ether')} ETH")
    print("-" * 60)

    time.sleep(INTERVALO_SEGUNDOS)
