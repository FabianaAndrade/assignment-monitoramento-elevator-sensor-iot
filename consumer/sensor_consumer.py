from kafka import KafkaConsumer
import os
from dotenv import load_dotenv
import json
from utils.Logger import Logger
from database.elevator_event_db import ElevatorEventDB
from utils.elevator_models import ElevatorEvent

class ElevatorEventConsumer:
    """
    Classe que gerencia o acesso dos eventos 
    registrados no topico do Kafka e
    os grava no banco de dados
    """
    def __init__(self, logger: Logger, topic: str, bootstrap_servers: str, group_id: str, elevator_event_db: ElevatorEventDB):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id=group_id,
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            api_version=(3, 8, 0),
        )
        self.elevator_event_db = elevator_event_db
        self.logger = logger

    def consume_events(self):
        for message in self.consumer:
            try:
                event = message.value
                self.logger.info(f"Evento consumido: {event}")
                if isinstance(event, dict):
                    self.__write_event_on_database(data_event=event)
            except json.JSONDecodeError as e:
                self.logger.error(f"Erro ao decodificar JSON: {e}")
            except Exception as e:
                self.logger.error(f"Erro ao processar o evento: {e}")

    def __write_event_on_database(self, data_event: dict):
        """
        Persiste o evento no banco de dados
        """
        try:
            event = ElevatorEvent(**data_event)
            self.elevator_event_db.insert_event(event)
            self.logger.info(f"Evento gravado no banco de dados")
        except Exception as e:
            self.logger.error(f"Erro ao gravar evento no banco de dados: {e}")


if __name__ == '__main__':
    load_dotenv()
    
    KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
    TOPIC_NAME = os.getenv("TOPIC_NAME", "elevator_events")
    GROUP_ID = os.getenv("GROUP_ID")
    DB_HOST = os.getenv("DB_HOST", "postgres")
    DB_PORT = os.getenv("DB_PORT", 5432)
    DB_NAME = os.getenv("DB_NAME", "elevator_events")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
    

    logger = Logger()
    logger.info("Iniciando o consumidor de eventos do elevador...")
    logger.info(f"Conectando ao Kafka Broker: {KAFKA_BROKER} no tópico: {TOPIC_NAME} com o grupo: {GROUP_ID}")
    
    elevator_event_db = ElevatorEventDB(
        db_host=DB_HOST,
        db_port=DB_PORT,
        db_name=DB_NAME,
        db_user=DB_USER,
        db_password=DB_PASSWORD
    )
    
    consumer = ElevatorEventConsumer(logger=logger,
                                     topic=TOPIC_NAME,
                                     bootstrap_servers=KAFKA_BROKER,
                                     group_id=GROUP_ID,
                                     elevator_event_db=elevator_event_db)
    consumer.consume_events()