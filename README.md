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

Tópico kafka: Gencia a transmissão das mensagens por streaming

Consumer: Captura as mensagens dispobilizadas no tópico e persiste no banco de dados

PostgreSQL: Base da dos relacional para persistencia dos dados

Metabase: ferramenta open source para visualização e monitoramento dos eventos






















