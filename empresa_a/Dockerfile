FROM python:3.10-slim
WORKDIR /app/app
COPY ./app /app/app
COPY requirements.txt /app
WORKDIR /app/app
RUN pip install --no-cache-dir -r /app/requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
