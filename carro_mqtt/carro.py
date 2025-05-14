import json
import random
import time
import paho.mqtt.client as mqtt

CAR_ID = f"carro-{random.randint(1000, 9999)}"
BROKER = "broker"  # nome do serviço no docker-compose
PORT = 1883
TOPIC_PUB = "carros/status"
TOPIC_SUB = f"carros/{CAR_ID}/resposta"

def on_connect(client, userdata, flags, rc):
    print(f"[{CAR_ID}] Conectado com código {rc}")
    client.subscribe(TOPIC_SUB)

def on_message(client, userdata, msg):
    print(f"[{CAR_ID}] Mensagem recebida: {msg.payload.decode()}")

client = mqtt.Client(CAR_ID)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT)

client.loop_start()

try:
    while True:
        status = {
            "id": CAR_ID,
            "bateria": random.randint(10, 100),
            "tendencia": random.choice(["descarga_rapida", "descarga_lenta"]),
            "rota": ["João Pessoa", "Maceió", "Sergipe", "Feira de Santana"]
        }
        print(f"[{CAR_ID}] Publicando status...")
        client.publish(TOPIC_PUB, json.dumps(status))
        time.sleep(10)
except KeyboardInterrupt:
    print("Encerrando...")
    client.loop_stop()
    client.disconnect()
