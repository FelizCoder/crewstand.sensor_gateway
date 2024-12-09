import os
from typing import List
from pydantic import Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

from models import ValueRange


current_file_directory = os.path.dirname(os.path.abspath(__file__))
env_file = os.path.join(
    current_file_directory,
    ".env.example",
)


class Config(BaseSettings):
    backend_sensor_url: HttpUrl
    log_level: str = "INFO"
    read_interval_s: float = Field(
        default=1,
        gt=0,
    )
    sensor_count: int = Field(
        default=1,
        gt=0,
        le=2,
    )
    serial_baud_rate: int = 192000
    serial_port: str
    voltage_range: ValueRange = (0.0, 3.3)
    measurement_range: List[ValueRange] = [(0.0, 100.0)]

    model_config = SettingsConfigDict(env_file=env_file)

    def __init__(self, **values):
        super().__init__(**values)
        if self.sensor_count != len(self.measurement_range):
            raise ValueError(
                f"measurement_range must have exactly as much items as sensor_count={self.sensor_count} items."
            )


settings = Config()
