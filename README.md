
# ⚡ Recarga Distribuída de Veículos Elétricos

Este projeto apresenta uma arquitetura distribuída para planejamento e execução de **reservas atômicas** em pontos de recarga de veículos elétricos (VEs), cobrindo **múltiplas empresas e estados**. A aplicação simula um ecossistema realista onde empresas diferentes, com sistemas independentes, colaboram para garantir o trajeto completo de um usuário, evitando falhas por indisponibilidade de recarga.

## 🎯 Motivação

A adoção de VEs esbarra em desafios como a **ansiedade de autonomia**, causada pela incerteza da disponibilidade de pontos de recarga ao longo de rotas longas. Cada ponto pertence a empresas distintas, exigindo múltiplos cadastros, apps e sistemas incompatíveis.

Este sistema resolve o problema permitindo que o usuário, ao iniciar uma viagem, reserve **todos os pontos da rota de forma atômica**, ou seja, **ou todos são garantidos ou nenhum é reservado**, com reversão completa em caso de falha.

## 🧱 Arquitetura Geral

- **Simulador de Veículos**: clientes MQTT (Python) publicam mensagens sobre rotas e estado de bateria.
- **Mosquitto Broker**: gerencia a comunicação MQTT entre veículos e servidores.
- **Servidores REST (FastAPI)**:
  - Representam empresas A, B e C
  - Cada um gerencia seus pontos de recarga e banco de dados local
  - Comunicação entre si via REST para coordenar reservas distribuídas
- **Docker Compose**: orquestra todos os componentes em contêineres isolados e interconectados.

## 🔄 Fluxo de Funcionamento

1. Um carro simulado gera uma **rota** com 3 pontos de recarga, um em cada servidor (empresa).
2. A rota é publicada via MQTT no tópico `veiculo/{id}/requisicao`.
3. O servidor que recebe a requisição atua como **coordenador** e inicia uma transação distribuída.
4. Cada ponto é reservado temporariamente (`/reserva-temporaria`).
5. Se todos os pontos forem reservados com sucesso, o coordenador envia `/confirmar-reserva`.
6. Se algum falhar, todos recebem `/cancelar-reserva` e desfazem a reserva.

## 📡 Comunicação

### MQTT (Carro → Servidor)
- `veiculo/{id}/status` – status periódico do carro (localização, bateria)
- `veiculo/{id}/requisicao` – rota solicitada
- `servidor/{id}/resposta` – resultado da reserva

### REST (Servidor ↔ Servidor)
Endpoints REST expostos em cada servidor:
- `GET /disponibilidade`  
  Retorna os pontos de recarga disponíveis.

- `POST /reserva-temporaria`  
  Reserva um ponto de recarga por tempo limitado. Recebe ID da sessão e dados do veículo.

- `POST /confirmar-reserva`  
  Finaliza a reserva temporária, tornando-a permanente.

- `DELETE /cancelar-reserva`  
  Cancela a reserva temporária.

## 🧪 Protocolo de Reserva Atômica – 2PC

O protocolo **Two-Phase Commit (2PC)** foi implementado para garantir atomicidade nas reservas:

- **Fase 1 – Preparação:**  
  O coordenador envia a solicitação de reserva temporária para todos os pontos.

- **Fase 2 – Commit ou Rollback:**  
  Se todos responderem OK, o coordenador envia `commit`.  
  Caso algum falhe, ele envia `rollback` para todos.

## ⚙️ Tecnologias Utilizadas

| Tecnologia       | Uso                                |
|------------------|-------------------------------------|
| Python 3.10+     | Lógica dos servidores e simulador   |
| FastAPI          | API REST entre empresas             |
| paho-mqtt        | Cliente MQTT dos carros             |
| Mosquitto        | Broker MQTT                         |
| Docker           | Contêineres para cada componente    |
| Docker Compose   | Orquestração do ambiente completo   |
| Insomnia/Postman | Testes manuais de API REST          |

## 📦 Execução

### Requisitos
- Docker instalado
- Docker Compose instalado

### Passos

```bash
# Clonar o repositório
git clone https://github.com/seuusuario/seurepo.git
cd seurepo

# Subir todo o ambiente
docker-compose up --build
```

Acesse os serviços nos seguintes endpoints:

- Empresa A: http://localhost:8001
- Empresa B: http://localhost:8002
- Empresa C: http://localhost:8003

## 🛠 Organização do Repositório

```
.
├── carro/
│   ├── carro.py                # Inicialização do cliente MQTT
│   ├── gerar_rota.py           # Geração de rotas fictícias
│   └── simulador_carros.py     # Lógica principal do simulador
├── empresa_a/
│   └── app/
├── empresa_b/
│   └── app/
├── empresa_c/
│   └── app/
├── mosquitto/
│   └── config/
├── docker-compose.yml
└── README.md
```

## 🚗 Simulação de Veículos

Os scripts Python no diretório `carro/` simulam diferentes carros com:

- IDs únicos
- Rotas de 3 pontos
- Estado de bateria variável
- Publicação automática de mensagens MQTT

## 📈 Resultados Esperados

- Reservas 100% atômicas entre empresas com diferentes servidores
- Rollback distribuído funcional em caso de falha
- Comunicação MQTT eficiente e assíncrona com feedback para o cliente
- Sistema modular e escalável com Docker

## 📚 Licença e Autoria

Projeto desenvolvido para a disciplina de Sistemas Distribuídos (TEC502) no LARSID – 2025.  
Uso acadêmico e educacional.

Autores:  
-  Fernanda Marinho Silva
-  Mirela Almeida Mascarenhas
-  Vitor Augusto Novaes de Jesus
