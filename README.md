
```markdown
# ⚡ Sistema de Recarga de Veículos Elétricos baseado em Blockchain

Este projeto propõe uma solução tecnológica inovadora para a gestão de recarga de veículos elétricos (VEs), utilizando **blockchain privada**, **contratos inteligentes (smart contracts)** e uma arquitetura de **microsserviços**. Ele simula a interação entre empresas de recarga e veículos de forma autônoma, registrando todas as transações de forma imutável e auditável na blockchain Ethereum, por meio da biblioteca **Web3.py**.

---

## 📘 Motivação e Objetivo

Com o crescimento da mobilidade elétrica, surge a necessidade de sistemas seguros, transparentes e descentralizados para gerenciar a recarga de veículos. A tecnologia **blockchain** oferece um ambiente confiável para esse tipo de aplicação, permitindo:

- Registro imutável de transações (reserva, recarga, pagamento)
- Redução de fraudes
- Eliminação de intermediários
- Auditoria completa das operações

O objetivo deste projeto é construir um **protótipo funcional** que simule esse ecossistema de recarga, demonstrando o potencial da blockchain para garantir a confiabilidade e automação do processo.

---

## 🧩 Arquitetura do Sistema

O sistema é dividido em **três microsserviços principais**, orquestrados via **Docker Compose**:

### 1. Blockchain Node (Ganache)
- Blockchain Ethereum privada local
- Contrato inteligente `ChargePoint.sol` implantado via `deploy.py`
- Contas pré-financiadas para testes
- Registra todas as ações de recarga de forma imutável

### 2. Serviço da Empresa (API - FastAPI)
- Fornece endpoints REST para:
  - Cadastro de empresas
  - Solicitação de reserva
  - Início e fim de recarga
- Interage com o contrato inteligente utilizando Web3.py
- Responsável por verificar disponibilidade e validar operações

### 3. Simulador de Carros (Scripts Python)
- Simula múltiplos veículos elétricos operando em paralelo
- Gera rotas aleatórias e solicita pontos de recarga
- Realiza pagamentos diretamente na blockchain
- Utiliza `carro.py`, `gerar_rota.py` e `consultar_rota_carro.py`

---

## 📦 Estrutura do Projeto

```

PBL-TEC502-P2-main/
├── blockchain/

│   ├── contracts/               # Contrato ChargePoint.sol
│   └── scripts/                 # Scripts de deploy e interação com o contrato

├── carro/
│   ├── carro.py                 # Simulação dos carros
│   ├── gerar\_rota.py            # Geração de rotas aleatórias
│   ├── consultar\_bloco.py       # Auditoria das transações
│   └── gerar\_historico.py       # Armazena histórico de simulações

├── empresa/
│   └── main.py                  # API REST da empresa
├── docker-compose.yml           # Orquestração dos serviços
├── requirements.txt             # Dependências Python
└── README.md

````

---

## 🔄 Ciclo de Vida de uma Recarga

1. **Veículo inicia a simulação** e gera uma rota
2. **Solicita reserva** em um ponto de recarga via `/reserva/fazer`
3. **API valida disponibilidade** e registra a reserva no contrato inteligente (`fazerReserva`)
4. **Veículo chega ao ponto** e inicia a recarga via `/recarga/iniciar`
5. **Ao finalizar a recarga**, registra a operação com `/recarga/finalizar`
6. **Pagamento é feito** diretamente na blockchain usando `pagarReserva`

Todas essas etapas geram **transações blockchain** visíveis e auditáveis.

---

## 🧪 Testes e Auditoria

Você pode testar manualmente os endpoints com **Postman** ou inspecionar os registros com:

- `interact.py` – Consulta estados e eventos no contrato
- `consultar_bloco.py` – Acessa os blocos minerados
- `historico_simulacao.txt` – Armazena os logs das execuções

---

## 🚀 Como Executar

### Pré-requisitos

- Docker e Docker Compose
- Python 3.10+ (apenas para testes externos)

### Execução

```bash
docker-compose up --build
````

Após a execução:

* O contrato será automaticamente implantado
* A API ficará disponível em `http://localhost:8000`
* Carros serão simulados automaticamente

---

## 📉 Resultados Obtidos

* Sistema funcional, com múltiplos veículos interagindo com a API e blockchain
* Confirmação de que todas as transações foram registradas de forma imutável
* Validação do comportamento autônomo e seguro dos contratos inteligentes

Logs típicos:

```
INFO:carro:Carro CAR-001: Iniciando simulação.
INFO:carro:Reserva no posto 1 realizada com sucesso.
INFO:carro:Iniciando recarga no posto 1...
INFO:carro:Recarga finalizada para o carro CAR-001 no posto 1. Custo: X.XX.
```

---

## 🚧 Limitações

* Simulação simplificada (sem consumo energético real)
* Rede blockchain com um único nó (Ganache)
* Ausência de interface gráfica
* Transações sem custo de gás (por ser ambiente local)

---

## 💡 Trabalhos Futuros

* ✅ Interface gráfica para usuários e operadores
* ✅ Deploy do contrato em redes públicas (Sepolia, Goerli)
* ✅ Integração com gateways de pagamento reais
* ✅ Simulação com consumo de bateria, tráfego e rotas reais

---

## 👥 Equipe

* Fernanda Marinho Silva
* Mirela Almeida Mascarenhas
* Vitor Augusto Novaes de Jesus

**UEFS – Universidade Estadual de Feira de Santana**
Disciplina: TEC502 MI – Projeto de Concorrência e Conectividade
Professora: Fabíola de Oliveira Pedreira

---

## 📜 Licença

Este projeto é de caráter acadêmico e está sob licença MIT. Uso livre para fins educacionais e de pesquisa.

---

```

---


