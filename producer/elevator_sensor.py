import random
from faker import Faker
  
class ElevatorSensor:
    """
    Classe que simula a emissao de dados 
    pelo sensor de um elevador
    """
    def __init__(self):
        self.fake_data = Faker()
        
    def generate_elevator_event(self) -> dict:
        event = {
            'timestamp': self.fake_data.date_time().isoformat(),
            'event_id': f'elevator_event_{random.randint(1000, 9999)}',
            'door_status': random.choice(['opened', 'closed']),
            'movement_detected': random.choice([True, False]),
            'duration_open_seconds': random.randint(1, 10),
            'person_passed': random.choice([True, False]),
            'sensor_id': f'door_{random.randint(1, 10):02}'
        }
        return event