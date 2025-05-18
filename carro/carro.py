import requests
from datetime import datetime, timedelta
from geopy.distance import geodesic

# 👇 sua base de capitais e empresas
CAPITAIS_BRASIL = [
    {"cidade": "João Pessoa", "uf": "PB", "latitude": -7.11509, "longitude": -34.8641, "empresa": "empresa_c", "ponto_id": "joao_pessoa01"},
    {"cidade": "Recife", "uf": "PE", "latitude": -8.04756, "longitude": -34.877, "empresa": "empresa_b", "ponto_id": "recife01"},
    {"cidade": "Aracaju", "uf": "SE", "latitude": -10.9472, "longitude": -37.0731, "empresa": "empresa_b", "ponto_id": "aracaju01"},
    {"cidade": "Maceió", "uf": "AL", "latitude": -9.66599, "longitude": -35.735, "empresa": "empresa_b", "ponto_id": "maceio01"},
    {"cidade": "Salvador", "uf": "BA", "latitude": -12.9718, "longitude": -38.5011, "empresa": "empresa_b", "ponto_id": "salvador01"},
    {"cidade": "Brasília", "uf": "DF", "latitude": -15.7797, "longitude": -47.9297, "empresa": "empresa_a", "ponto_id": "brasilia01"},
    # Adicione as demais capitais conforme necessário
]

def encontrar_cidade(cidade_nome):
    for c in CAPITAIS_BRASIL:
        if c["cidade"].lower() == cidade_nome.lower():
            return c
    return None

def gerar_rota(origem_nome, destino_nome, carro_id="carro123", hora_inicio_str="2025-05-13T08:00:00"):
    origem = encontrar_cidade(origem_nome)
    destino = encontrar_cidade(destino_nome)

    if not origem or not destino:
        raise ValueError("Origem ou destino não encontrados nas capitais.")

    cidades_ordenadas = sorted(
        CAPITAIS_BRASIL,
        key=lambda c: geodesic((origem["latitude"], origem["longitude"]), (c["latitude"], c["longitude"])).km
    )

    i_origem = cidades_ordenadas.index(origem)
    i_destino = cidades_ordenadas.index(destino)
    if i_origem > i_destino:
        trecho = cidades_ordenadas[i_destino:i_origem + 1][::-1]
    else:
        trecho = cidades_ordenadas[i_origem:i_destino + 1]

    rota_requisicao = []
    hora_inicio = datetime.fromisoformat(hora_inicio_str)
    for i, cidade in enumerate(trecho):
        janela_inicio = hora_inicio + timedelta(hours=i * 2)
        janela_fim = janela_inicio + timedelta(hours=1)

        ponto_url = f"http://{cidade['empresa']}:8000#{cidade['ponto_id']}"
        rota_requisicao.append({
            "carro_id": carro_id,
            "ponto_id": ponto_url,
            "janela_inicio": janela_inicio.isoformat(),
            "janela_fim": janela_fim.isoformat()
        })

    return rota_requisicao, origem["empresa"]

def requisitar_rota(rota_json, empresa_origem):
    url_rota = f"http://{empresa_origem}:8000/rota"
    try:
        response = requests.post(url_rota, json=rota_json)
        if response.status_code == 200:
            print("✅ Rota reservada com sucesso:")
            print(response.json())
        else:
            print("❌ Falha na reserva:")
            print(response.status_code, response.text)
    except Exception as e:
        print("❌ Erro ao conectar com servidor de origem:", e)

def main():
    carro_id = input("🆔 ID do carro: ").strip()
    origem = input("🚗 Cidade de origem: ").strip()
    destino = input("🎯 Cidade de destino: ").strip()

    try:
        rota_json, empresa_origem = gerar_rota(origem, destino, carro_id)
        print("\n📦 Rota planejada:")
        for parada in rota_json:
            print(parada)

        confirmar = input("\nDeseja reservar esta rota? (s/n): ").strip().lower()
        if confirmar == "s":
            requisitar_rota(rota_json, empresa_origem)
        else:
            print("❌ Reserva cancelada.")
    except ValueError as e:
        print("⚠️ Erro:", e)

if __name__ == "__main__":
    main()
