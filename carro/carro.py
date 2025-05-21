import requests
import random
import string
from gerar_rota import gerar_rota_autonoma

def gerar_id_carro(): # gera id aleatorio para o carro
    return "carro_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))

def main():
    carro_id = gerar_id_carro()
    print(f"🆔 ID do carro: {carro_id}")

    origem = input("🚗 Origem (ex: João Pessoa): ").strip()
    destino = input("🎯 Destino (ex: Aracaju): ").strip()
    bateria = int(input("🔋 Bateria inicial (0-100): ").strip())

    try:
        rota, empresa_origem = gerar_rota_autonoma(origem, destino, carro_id, bateria)
        print("\n📦 Rota planejada com base na bateria:")
        for p in rota:
            print(p)

        confirmar = input("\nDeseja reservar esta rota? (s/n): ").strip().lower()
        if confirmar != 's':
            print("🚫 Cancelado.")
            return

        response = requests.post(f"http://{empresa_origem}:8000/rota", json=rota)
        if response.status_code == 200:
            print("✅ Rota reservada com sucesso!")
        else:
            print(f"❌ Falha na reserva: {response.status_code} - {response.text}")

    except Exception as e:
        print("❌ Erro:", e)

if __name__ == "__main__":
    main()
