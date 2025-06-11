import os
import subprocess
import time

def docker_ativo(url="http://localhost:8001"):
    try:
        import requests
        requests.get(url, timeout=3)
        return True
    except Exception:
        return False

def rodar_simulacao():
    processo = subprocess.Popen(
        ["python3", "simulador_carros.py"],  
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )

    saida_completa = ""

    while True:
        linha = processo.stdout.readline()
        if not linha and processo.poll() is not None:
            break
        if linha:
            print(linha, end="")  
            saida_completa += linha

        if not docker_ativo():
            processo.terminate()
            break

    return saida_completa

def salvar_log_em_txt(texto, caminho="historico_simulacao.txt"):
    with open(caminho, "w") as f:
        f.write(texto)
    print(f"\n💾 Log salvo em '{caminho}'.")

def main():
    print("🔁 Aguardando serviços do Docker ficarem disponíveis...")
    while not docker_ativo():
        time.sleep(2)

    print("🚗 Iniciando simulação enquanto o Docker/Simulação estiver ativo...")
    log = rodar_simulacao()

    print("🛑 Docker parece ter parado. Salvando log...")
    salvar_log_em_txt(log)

if __name__ == "__main__":
    main()
