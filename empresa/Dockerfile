# Use uma imagem base do Python
FROM python:3.10-slim

# Instala o curl, necessário para o healthcheck do Docker Compose
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo de requisitos para o WORKDIR
COPY requirements.txt .

# Instala as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# --- CORREÇÃO APLICADA AQUI ---
# Copia o código da aplicação para uma subpasta 'app' dentro do WORKDIR
# Isso garante que a importação 'app.main' funcione corretamente
COPY ./app ./app

# A porta que a aplicação vai expor (o uvicorn será executado na porta 8000)
EXPOSE 8000