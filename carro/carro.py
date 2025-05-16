import random
import time
import json
import paho.mqtt.client as mqtt

CARRO_ID = "carro123"
BROKER = "broker_mqtt"
TOPICO_STATUS = "carros/status"

def gerar_status_bateria():
    return {
        "carro_id": CARRO_ID,
        "nivel_bateria": random.randint(10, 100),
        "tendencia_descarga": random.choice(["rapida", "lenta"]),
        "localizacao": random.choice(["João Pessoa", "Maceió", "Aracaju"])
    }

def publicar_status(client):
    while True:
        status = gerar_status_bateria()
        print(f"Publicando: {status}")
        client.publish(TOPICO_STATUS, json.dumps(status))
        time.sleep(5)

if __name__ == "__main__":
    time.sleep(10)  # espera o broker iniciar
    client = mqtt.Client()
    try:
        client.connect(BROKER, 1883, 60)
    except Exception as e:
        print(f"Erro ao conectar no broker: {e}")
        exit(1)
    client.loop_start()
    publicar_status(client)
