FROM python:3.10-slim

WORKDIR /app

# Copia o requirements.txt de dentro do diretorio empresa_comum
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia a aplicacao (que esta em empresa_comum/app) para o WORKDIR (/app)
COPY app/ /app/

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]