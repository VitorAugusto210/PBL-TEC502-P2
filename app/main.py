from fastapi import FastAPI
from app.routers import recarga
import threading
import json
import paho.mqtt.client as mqtt

app = FastAPI(title="Servidor de Recarga")
app.include_router(recarga.router, prefix="/recarga")

# === MQTT Listener ===

def on_connect(client, userdata, flags, rc):
    print("[MQTT] Conectado ao broker com código:", rc)
    client.subscribe("carros/status")

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    print(f"[MQTT] Recebido de {data['id']}: bateria {data['bateria']}%, rota {data['rota']}")

    resposta = {
        "proximo_ponto": "Maceió",
        "mensagem": "Reserva feita para você em Maceió!"
    }

    topic_resposta = f"carros/{data['id']}/resposta"
    client.publish(topic_resposta, json.dumps(resposta))
    print(f"[MQTT] Resposta enviada para {topic_resposta}")

def start_mqtt_listener():
    client = mqtt.Client("servidor-api")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("broker", 1883)
    client.loop_forever()

# Inicia o MQTT em paralelo com o FastAPI
threading.Thread(target=start_mqtt_listener, daemon=True).start()
