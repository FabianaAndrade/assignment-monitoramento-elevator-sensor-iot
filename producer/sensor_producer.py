from kafka import KafkaProducer
from dotenv import load_dotenv
import os
import random
from pydantic import ValidationError
import json
import time
from utils.Logger import Logger
from utils.elevator_models import ElevatorEvent
from producer.elevator_sensor import ElevatorSensor


class SensorProducer:
    """
    Produtor de eventos de elevador para o Kafka, 
    inicia a geração de eventos a partir do sensor e 
    envia para o tópico kafka
    """
    def __init__(self, sensor: ElevatorSensor, logger: Logger, topic: str, bootstrap_servers: str):
        self.logger = logger
        self.sensor = sensor
        self.topic = topic
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8'),
            key_serializer=lambda k: k.encode('utf-8'),
            api_version=(3, 8, 0) 
        )

    def produce_events(self) -> None:
        while True:
            try:
                event_data = self.sensor.generate_elevator_event()
                event = ElevatorEvent(**event_data)            
                self.logger.info(f"Produzindo evento: {event}")
                key = event_data["sensor_id"]
                self.producer.send(self.topic, key=key, value=dict(event))
                self.producer.flush()
                time.sleep(random.uniform(0.5, 2.0))
            except ValidationError as e:
                self.logger.error(f"Erro de validação: {e.json()}")
            except Exception as e:
                self.logger.error(f"Erro ao produzir evento: {e}")


    
if __name__ == "__main__":
    load_dotenv()
    KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
    TOPIC_NAME = os.getenv("TOPIC_NAME", "elevator_events")

    logger_instance = Logger()
    logger_instance.info("iniciando a captura de eventos do sensor de elevador...")
    logger_instance.info(f"conectando ao Kafka Broker: {KAFKA_BROKER} no tópico: {TOPIC_NAME}")
    sensor = ElevatorSensor()
    producer = SensorProducer(sensor = sensor,
                              logger=logger_instance,
                              topic=TOPIC_NAME,
                              bootstrap_servers=KAFKA_BROKER)
    producer.produce_events()