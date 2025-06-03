import requests
from datetime import datetime

EMPRESAS = {
    "empresa_a": "http://localhost:8000",
    "empresa_b": "http://localhost:8001",
    "empresa_c": "http://localhost:8002",
}

def buscar_reservas_por_carro(carro_id):
    reservas = []

    for nome, url_base in EMPRESAS.items():
        try:
            res = requests.get(f"{url_base}/reservas/carro/{carro_id}")
            if res.status_code == 200:
                dados = res.json()
                for r in dados:
                    r["empresa"] = nome
                    reservas.append(r)
        except Exception as e:
            print(f"⚠️ Erro ao consultar {nome}: {e}")

    # Ordenar pela janela_inicio
    reservas.sort(key=lambda r: datetime.fromisoformat(r["janela_inicio"]))
    return reservas

def exibir_rota(carro_id):
    reservas = buscar_reservas_por_carro(carro_id)
    if not reservas:
        print(f"🚫 Nenhuma reserva encontrada para {carro_id}")
        return

    print(f"\n📍 Rota do carro {carro_id}:\n")
    for r in reservas:
        print(f"  🏢 {r['empresa']} | 🛑 Ponto: {r['ponto_id']} | ⏰ {r['janela_inicio']} → {r['janela_fim']}")

if __name__ == "__main__":
    carro_id = input("Digite o ID do carro: ").strip()
    exibir_rota(carro_id)
