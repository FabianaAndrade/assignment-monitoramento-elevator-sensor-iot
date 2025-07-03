'''
Testes unitarios para o consumidor de eventos e 
produtor de eventos do elevador.
'''
import pytest
from pydantic import ValidationError
from unittest.mock import MagicMock, patch
from consumer.sensor_consumer import ElevatorEventConsumer
from utils.elevator_models import ElevatorEvent
from producer.sensor_producer import SensorProducer


@pytest.fixture
def mock_logger():
    return MagicMock()


@pytest.fixture
def mock_db():
    db = MagicMock()
    db.insert_event = MagicMock()
    return db


@pytest.fixture
def sample_event():
    return {
        "timestamp": "2025-07-03T14:00:00",
        "event_id": "elevator_event_1234",
        "door_status": "opened",
        "movement_detected": True,
        "duration_open_seconds": 5,
        "person_passed": True,
        "sensor_id": "door_01"
    }


class TestElevatorEventConsumer:
    def elevator_consumer(self, mock_logger, mock_db):
        return ElevatorEventConsumer(
            logger=mock_logger,
            topic="test_topic",
            bootstrap_servers="localhost:9092",
            group_id="test_group",
            elevator_event_db=mock_db
        )
    
    def test_init_consumer(self, mock_logger, mock_db):
        consumer = self.elevator_consumer(mock_logger, mock_db)
        assert consumer.logger == mock_logger
        assert consumer.elevator_event_db == mock_db

    def test_consume_single_event(self, mock_logger, mock_db, sample_event):
        mock_message = MagicMock()
        mock_message.value = sample_event

        with patch("consumer.sensor_consumer.KafkaConsumer") as MockKafkaConsumer:
            MockKafkaConsumer.return_value = [mock_message]

            consumer = self.elevator_consumer(mock_logger, mock_db)
            consumer.consume_events()

            mock_logger.info.assert_any_call(f"Evento consumido: {sample_event}")
            mock_logger.info.assert_any_call("Evento gravado no banco de dados")
            mock_db.insert_event.assert_called_once()
            args, kwargs = mock_db.insert_event.call_args
            assert isinstance(args[0], ElevatorEvent)
            assert args[0].event_id == "elevator_event_1234"

    def test_consume_invalid_event(self, mock_logger, mock_db):
        mock_message = MagicMock()
        mock_message.value = {"invalid_key": "invalid_value"}

        with patch("consumer.sensor_consumer.KafkaConsumer") as MockKafkaConsumer:
            MockKafkaConsumer.return_value = [mock_message]

            consumer = ElevatorEventConsumer(
                logger=mock_logger,
                topic="test_topic",
                bootstrap_servers="localhost:9092",
                group_id="test_group",
                elevator_event_db=mock_db
            )

            consumer.consume_events()
            mock_db.insert_event.assert_not_called()

class TestSensorProducer:
    def test_produce_event(self, mock_logger, sample_event):
        sensor_mock = MagicMock()
        sensor_mock.generate_elevator_event.return_value = sample_event

        with patch("producer.sensor_producer.KafkaProducer") as MockKafkaProducer:
            mock_producer_instance = MockKafkaProducer.return_value

            producer = SensorProducer(
                sensor=sensor_mock,
                logger=mock_logger,
                topic="test_topic",
                bootstrap_servers="localhost:9092"
            )
            with patch("time.sleep", return_value=None):
                sensor_mock.generate_elevator_event.side_effect = [sample_event, KeyboardInterrupt()]
                try:
                    producer.produce_events()
                except KeyboardInterrupt:
                    pass
            

            mock_producer_instance.send.assert_called_once()
            mock_logger.info.assert_any_call(f"Produzindo evento: {ElevatorEvent(**sample_event)}")

    def test_produce_invalid_event(self, mock_logger):
        invalid_event = {
            "timestamp": "2025-07-03T14:00:00",
            "event_id": "elevator_event_1234",
            "door_status": "opened",
            "movement_detected": False,
            "duration_open_seconds": 5,
            "person_passed": True,  # invalido, pois 'movement_detected' é False e não deveria haver pessoa passando
            "sensor_id": "door_01"
        }

        sensor_mock = MagicMock()
        sensor_mock.generate_elevator_event.return_value = invalid_event

        with patch("producer.sensor_producer.KafkaProducer") as MockKafkaProducer:
            mock_producer_instance = MockKafkaProducer.return_value

            producer = SensorProducer(
                sensor=sensor_mock,
                logger=mock_logger,
                topic="test_topic",
                bootstrap_servers="localhost:9092"
            )
            with patch("time.sleep", return_value=None):
                sensor_mock.generate_elevator_event.side_effect = [invalid_event, KeyboardInterrupt()]
                try:
                    producer.produce_events()
                except KeyboardInterrupt:
                    pass
            mock_producer_instance.send.assert_not_called()
            