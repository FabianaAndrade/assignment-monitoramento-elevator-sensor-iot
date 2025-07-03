## assignment-monitoramento-elevator-sensor-iot
# Monitoramento streaming de Sensor IOT de Elevador 

Este fluxo aborda uma situação-problema para o transporte de dados em tempo-real (streaming) de um sensor IOT de um elevador. 
O sistema gera dados com eventos ocorridos no elevador, são emitidas informações como momento do evento, se a porta abriu ou não, se uma pessoa passou pela porta, se houve um movimento detectado, quanto tempo a porta ficou aberta etc.
Essas informações do sensor precisam ser capturadas e persistidas para posterior analise e geração de insigths sobre o funcionamento do elevador, principais eventos que ocorrem, para que o time de gestão predial manter o monitoramento.


Dado essa situação-problema foi desenvolvido essse fluxo streaming para transporte dos dados.
A solução consiste em implementar o produtor, ou seja, o sensor do elevador que produz os dados, que disponibiliza (publica) os eventos gerados em um tópico kafka para que o consumidor dos eventos capture essas informações em tempo-real e persista os dados em um banco de dados.

# Arquitetura-macro
![Sem título-2025-07-02-2113](https://github.com/user-attachments/assets/46c37a66-d9f2-422b-9d0c-0247a72a0d7c)

Producer: Gerencia produção dos dados do sensor e os dispobiliza no tópico Kafka

Tópico kafka: Gerenncia a transmissão das mensagens por streaming

Consumer: Captura as mensagens dispobilizadas no tópico e persiste no banco de dados

PostgreSQL: Base da dos relacional para persistencia dos dados

Metabase: ferramenta open source para visualização e monitoramento dos eventos


```text
/app
│
├── producer/
│   ├── __init__.py
│   ├── elevator_sensor.py
│   └── sensor_producer.py        # Produtor de eventos
│ 
├── consumer/
│   ├── __init__.py
│   └── sensor_consumer.py        # consumidor eventos
│
├── database/
│   ├── __init__.py
│   └── elevator_event_db.py      # persistencia dos eventos
│
├── utils/
│   ├── __init__.py
│   ├── Logger.py                 # Classe utilitária para logging
│   └── elevator_models.py        # Base model para validar um event emitido
│ 
├── tests/
│   ├── __init__.py
│   └── tests.py                  # testes unitarios
│
├── init-db/
│   └── init-metabase-db.sql      # Criacao do db para o metabase
│
├── Dockerfile.producer           # Dockerfile para o produtor
├── Dockerfile.consumer           # Dockerfile para o consumidor
└── docker-compose.yml            # Orquestração dos serviços com Docker
```

# Utilização

Tenha previamente instalado:
```text
- Docker e Docker-compose
```

1. Clone o repo
```text
- git clone 
```
2. Defina as váriaveis de ambientes
```text
- git clone 
```
3. Inicie os containers
```text
docker-compose up --build 
```
4. Navegação
-Para acompanhar pela UI do Kafka as mensagens transmitidas: http://localhost:8080 (caminho default)
-Para acompanhar o dashboard com metricas de eventos no Metabase: http://localhost:3000 (caminho default)




















