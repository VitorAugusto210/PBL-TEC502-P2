import json
import random
import string
import time
import paho.mqtt.client as mqtt

carro_id = "carro_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
BROKER = "broker"
PORT = 1883
TOPIC_PUB = "carros/solicitacao"
TOPIC_SUB = f"carros/{carro_id}/rota"

rota_recebida = None

def on_connect(client, userdata, flags, rc):
    print(f"[{carro_id}] Conectado ao broker (código {rc})")
    client.subscribe(TOPIC_SUB)

def on_message(client, userdata, msg):
    global rota_recebida
    print(f"[{carro_id}] Rota recebida!")
    try:
        rota_recebida = json.loads(msg.payload.decode())
    except Exception as e:
        print(f"Erro ao decodificar a rota: {e}")

client = mqtt.Client(carro_id)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT)
client.loop_start()

try:
    origem = input("🚗 Origem (ex: João Pessoa): ").strip()
    destino = input("🎯 Destino (ex: Aracaju): ").strip()
    bateria = int(input("🔋 Bateria inicial (0-100): ").strip())

    mensagem = {
        "id": carro_id,
        "origem": origem,
        "destino": destino,
        "bateria": bateria
    }

    print(f"[{carro_id}] Enviando solicitação de rota...")
    client.publish(TOPIC_PUB, json.dumps(mensagem))

    timeout = 5 
    esperado = time.time() + timeout

    while rota_recebida is None and time.time() < esperado:
        time.sleep(0.5)

    if rota_recebida is None:
        print("❌ Tempo excedido aguardando a rota.")
    else:
        print("\n📦 Rota recebida:")
        for p in rota_recebida:
            print(p)

        confirmar = input("\nDeseja reservar esta rota? (s/n): ").strip().lower()
        if confirmar != 's':
            print("🚫 Reserva cancelada.")
        else:
            print("✅ (Simulação) Rota confirmada com sucesso!")

except Exception as e:
    print(f"❌ Erro inesperado: {e}")

finally:
    client.loop_stop()
    client.disconnect()
    print(f"[{carro_id}] Conexão encerrada.")
