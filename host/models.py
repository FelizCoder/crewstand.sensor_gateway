import time
from pydantic import BaseModel, Field


class SensorReading(BaseModel):
    """Base model for a sensor reading."""

    value: float
    timestamp_ns: int = Field(
        ...,
        description="Timestamp of the reading in nanoseconds since Epoch",
        examples=[1730906908814683100],
    )
    
    @classmethod
    def new_reading(cls, value: float) -> "SensorReading":
        timestamp_ns = time.time_ns()
        return cls(value=value, timestamp_ns=timestamp_ns)