import os
import time
import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTMessage

# --- CORREÇÃO APLICADA AQUI (Assinatura das funções) ---
# As funções de callback agora usam a assinatura da v2 da API.
def on_connect(client: mqtt.Client, userdata, flags, rc, properties):
    """Callback executado ao conectar ao broker."""
    if rc == 0:
        client_id = client._client_id.decode()
        print(f"Carro (ID: {client_id}) conectado ao broker MQTT com sucesso.")
        # Subscreve a um tópico genérico para receber rotas.
        client.subscribe("rota/+")
    else:
        print(f"Falha ao conectar ao broker, código de retorno: {rc}")

def on_message(client: mqtt.Client, userdata, msg: MQTTMessage):
    """Callback executado ao receber uma mensagem."""
    carro_id = client._client_id.decode()
    print(f"[{carro_id}] Rota recebida no tópico '{msg.topic}':")
    print(str(msg.payload.decode()))
    client.loop_stop()

def on_disconnect(client: mqtt.Client, userdata, rc, properties):
    """Callback para quando o cliente se desconecta."""
    carro_id = client._client_id.decode()
    print(f"[{carro_id}] Desconectado do broker MQTT.")

if __name__ == "__main__":
    carro_id = f"carro_{os.getpid()}"
    
    # --- CORREÇÃO APLICADA AQUI (Versão da API) ---
    # Usando a versão 2 da API de Callbacks.
    client = mqtt.Client(CallbackAPIVersion.VERSION2, carro_id)
    # ---------------------------------------------

    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    try:
        print(f"[{carro_id}] Tentando conectar ao broker MQTT em 'mosquitto:1883'...")
        client.connect("mosquitto", 1883, 60)
        client.loop_forever()
    except ConnectionRefusedError:
        print(f"[{carro_id}] Erro: Conexão recusada. O broker MQTT está acessível?")
    except OSError as e:
        print(f"[{carro_id}] Erro de rede: {e}. Verifique a rede do Docker.")
    except KeyboardInterrupt:
        print(f"[{carro_id}] Simulação interrompida pelo usuário.")
    except Exception as e:
        print(f"[{carro_id}] Ocorreu um erro inesperado: {e}")
    finally:
        client.disconnect()