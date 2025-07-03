from datetime import datetime
from pydantic import BaseModel, Field, model_validator
from typing import Literal

class ElevatorEvent(BaseModel):
    """
    Modelo Pydantic para representar
    eventos de elevador, validar estrutura aceita e
    garantir a logica dos campos.
    """
    timestamp: datetime = Field(..., description="Data e hora do evento")
    event_id: str = Field(..., description="ID do evento")
    door_status: Literal["opened", "closed"] = Field(..., description="Status da porta do elevador")
    duration_open_seconds: int = Field(..., ge=0, description="Duração em segundos que a porta ficou aberta")
    movement_detected: bool = Field(..., description="Se houve movimento detectado")
    person_passed: bool = Field(..., description="Se uma pessoa passou pela porta")
    sensor_id: str = Field(..., pattern=r"^door_\d{2}$", description="ID do sensor, ex: door_01")
    model_config = {
        "arbitrary_types_allowed": True
    }
    
    @model_validator(mode="after")
    def validate_logical_values(self) -> 'ElevatorEvent':
        """
        Valida algumas relações logicas basicas entre os campos do evento.
        - Se 'person_passed' é True, 'movement_detected' também deve ser True.
        - Se a porta está 'closed', 'duration_open_seconds' deve ser 0.
        - Se a porta está 'opened', 'duration_open_seconds' deve ser maior que 0.
        """
        if self.person_passed and not(self.movement_detected):
            raise ValueError("Se 'person_passed' é True, 'movement_detected' também deve ser True.")
        
        if self.door_status == "closed" and self.duration_open_seconds > 0:
            raise ValueError("Se a porta está 'closed', 'duration_open_seconds' deve ser 0.")
        
        if self.door_status == "opened" and self.duration_open_seconds <= 0:
            raise ValueError("Se a porta está 'opened', 'duration_open_seconds' deve ser maior que 0.")

        return self