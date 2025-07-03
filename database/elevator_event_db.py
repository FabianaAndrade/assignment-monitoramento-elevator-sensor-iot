import psycopg2
from utils.elevator_models import ElevatorEvent
import time

class ElevatorEventDB:
    """
    Classe para gerenciar a conexão com o banco de dados PostgreSQL
    que armazena os eventos do elevador.
    Gerenciona a criação da tabela e a inserção de novos eventos.
    """
    def __init__(self, db_host: str, db_port: str, db_name: str, db_user: str, db_password:str):
        while True:
                try:
                    self.conn = psycopg2.connect(
                    host=db_host,
                    port=db_port,
                    dbname=db_name,
                    user=db_user,
                    password=db_password
                    )
                    break
                except psycopg2.OperationalError as e:
                    time.sleep(3)
        self.__create_table()

    def __create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS elevator_events (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP NOT NULL,
            event_id VARCHAR(50) NOT NULL,
            door_status VARCHAR(10) NOT NULL,
            duration_open_seconds INTEGER NOT NULL,
            movement_detected BOOLEAN NOT NULL,
            person_passed BOOLEAN NOT NULL,
            sensor_id VARCHAR(20) NOT NULL
        );
        """
        with self.conn.cursor() as cur:
            cur.execute(query)
            self.conn.commit()

    def insert_event(self, event: ElevatorEvent):
        query = """
        INSERT INTO elevator_events (
            timestamp, event_id, door_status, duration_open_seconds,
            movement_detected, person_passed, sensor_id
        ) VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        values = (
            event.timestamp,
            event.event_id,
            event.door_status,
            event.duration_open_seconds,
            event.movement_detected,
            event.person_passed,
            event.sensor_id
        )
        with self.conn.cursor() as cur:
            cur.execute(query, values)
            self.conn.commit()
