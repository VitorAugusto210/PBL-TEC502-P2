from datetime import datetime, timedelta
from geopy.distance import geodesic
import json

# geolocalizacao de capitais com empresa e pontos associados a ela
CAPITAIS_BRASIL = [
    {"cidade": "João Pessoa", "latitude": -7.115, "longitude": -34.8641, "empresa": "empresa_c", "ponto_id": "jp01"},
    {"cidade": "Recife", "latitude": -8.0476, "longitude": -34.877, "empresa": "empresa_b", "ponto_id": "pe01"},
    {"cidade": "Maceió", "latitude": -9.6659, "longitude": -35.735, "empresa": "empresa_b", "ponto_id": "mc01"},
    {"cidade": "Aracaju", "latitude": -10.9472, "longitude": -37.0731, "empresa": "empresa_b", "ponto_id": "aj01"},
    {"cidade": "Salvador", "latitude": -12.9718, "longitude": -38.5011, "empresa": "empresa_b", "ponto_id": "sv01"},
]

def encontrar_cidade(nome):
    for c in CAPITAIS_BRASIL:
        if c["cidade"].lower() == nome.lower():
            return c
    return None

def calcular_autonomia_km(bateria_percentual):
    return (bateria_percentual / 100) * 400  # 100% = 400 km

def gerar_rota_autonoma(origem_nome, destino_nome, carro_id="carro123", bateria_inicial=100):
    origem = encontrar_cidade(origem_nome)
    destino = encontrar_cidade(destino_nome)
    if not origem or not destino:
        raise ValueError("Origem ou destino inválidos.")

    cidades_ordenadas = sorted(
        CAPITAIS_BRASIL,
        key=lambda c: geodesic((origem["latitude"], origem["longitude"]), (c["latitude"], c["longitude"])).km
    )
    i_origem = cidades_ordenadas.index(origem)
    i_destino = cidades_ordenadas.index(destino)
    trecho = cidades_ordenadas[min(i_origem, i_destino):max(i_origem, i_destino)+1]
    if i_origem > i_destino:
        trecho = list(reversed(trecho))

    rota = []
    autonomia_restante_km = calcular_autonomia_km(bateria_inicial)
    distancia_acumulada = 0
    hora_inicio = datetime.now()

    for i in range(len(trecho)-1):
        cidade_atual = trecho[i]
        cidade_prox = trecho[i+1]
        distancia = geodesic(
            (cidade_atual["latitude"], cidade_atual["longitude"]),
            (cidade_prox["latitude"], cidade_prox["longitude"])
        ).km
        distancia_acumulada += distancia

        if distancia_acumulada >= autonomia_restante_km or i == 0:
            janela_inicio = hora_inicio + timedelta(hours=len(rota) * 2)
            janela_fim = janela_inicio + timedelta(hours=1)

            ponto_url = f"http://{cidade_atual['empresa']}:8000#{cidade_atual['ponto_id']}"
            rota.append({
                "carro_id": carro_id,
                "ponto_id": ponto_url,
                "janela_inicio": janela_inicio.isoformat(),
                "janela_fim": janela_fim.isoformat()
            })
            autonomia_restante_km = 400  # recarrega total
            distancia_acumulada = 0

    # adicionar a parada final
    janela_inicio = hora_inicio + timedelta(hours=len(rota) * 2)
    janela_fim = janela_inicio + timedelta(hours=1)
    ponto_url = f"http://{destino['empresa']}:8000#{destino['ponto_id']}"
    rota.append({
        "carro_id": carro_id,
        "ponto_id": ponto_url,
        "janela_inicio": janela_inicio.isoformat(),
        "janela_fim": janela_fim.isoformat()
    })
    print("📦 Rota gerada:")
    print(json.dumps(rota, indent=2))

    return rota, origem["empresa"]
