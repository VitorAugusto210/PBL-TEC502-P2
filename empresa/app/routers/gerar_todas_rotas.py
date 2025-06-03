from geopy.distance import geodesic
from datetime import datetime, timedelta

# 🔗 Base de capitais conectadas em ordem simplificada (você pode expandir!)
CAPITAIS = [
    {"cidade": "João Pessoa", "empresa": "empresa_a", "ponto_id": "jp01", "coords": (-7.115, -34.8641)},
    {"cidade": "Recife", "empresa": "empresa_b", "ponto_id": "pe01", "coords": (-8.0476, -34.877)},
    {"cidade": "Maceió", "empresa": "empresa_b", "ponto_id": "mc01", "coords": (-9.6659, -35.735)},
    {"cidade": "Aracaju", "empresa": "empresa_b", "ponto_id": "aj01", "coords": (-10.9472, -37.0731)},
    {"cidade": "Salvador", "empresa": "empresa_b", "ponto_id": "sv01", "coords": (-12.9718, -38.5011)},
]

# 🔄 Grafo implícito (baseado na ordem)
def cidades_vizinhas(cidade):
    idx = next((i for i, c in enumerate(CAPITAIS) if c["cidade"] == cidade), None)
    vizinhos = []
    if idx is not None:
        if idx > 0:
            vizinhos.append(CAPITAIS[idx - 1])
        if idx < len(CAPITAIS) - 1:
            vizinhos.append(CAPITAIS[idx + 1])
    return vizinhos

def distancia_km(c1, c2):
    return geodesic(c1["coords"], c2["coords"]).km

# 🔍 Busca todas as rotas possíveis com limite de autonomia
def buscar_rotas(origem, destino, autonomia_km):
    origem_cid = next((c for c in CAPITAIS if c["cidade"].lower() == origem.lower()), None)
    destino_cid = next((c for c in CAPITAIS if c["cidade"].lower() == destino.lower()), None)
    if not origem_cid or not destino_cid:
        raise ValueError("Origem ou destino inválido")

    rotas = []

    def dfs(caminho, visitados, autonomia_restante):
        atual = caminho[-1]
        if atual["cidade"] == destino_cid["cidade"]:
            rotas.append(list(caminho))
            return

        for viz in cidades_vizinhas(atual["cidade"]):
            if viz["cidade"] in visitados:
                continue
            dist = distancia_km(atual, viz)
            if dist <= autonomia_restante:
                dfs(caminho + [viz], visitados | {viz["cidade"]}, autonomia_km)
    
    dfs([origem_cid], {origem_cid["cidade"]}, autonomia_km)
    return rotas

# 🛠️ Monta formato JSON com janelas de tempo
def formatar_rotas(rotas_brutas, carro_id):
    rotas_formatadas = []
    hora = datetime.now()

    for rota in rotas_brutas:
        rota_formatada = []
        for i, cidade in enumerate(rota):
            janela_inicio = hora + timedelta(hours=i * 2)
            janela_fim = janela_inicio + timedelta(hours=1)
            rota_formatada.append({
                "carro_id": carro_id,
                "ponto_id": f"http://{cidade['empresa']}:8000#{cidade['ponto_id']}",
                "janela_inicio": janela_inicio.isoformat(),
                "janela_fim": janela_fim.isoformat()
            })
        rotas_formatadas.append(rota_formatada)

    return rotas_formatadas

# 🚀 Função principal
def gerar_todas_rotas(origem, destino, carro_id, autonomia_km=400):
    rotas_brutas = buscar_rotas(origem, destino, autonomia_km)
    return formatar_rotas(rotas_brutas, carro_id)
