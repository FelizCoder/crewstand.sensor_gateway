import os
from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


current_file_directory = os.path.dirname(os.path.abspath(__file__))
env_file = os.path.join(
    current_file_directory,
    ".env.example",
)


class Config(BaseSettings):
    read_interval_s: float = 1.0
    serial_port: str
    serial_baud_rate: int = 192000
    backend_sensor_url: HttpUrl

    model_config = SettingsConfigDict(env_file=env_file)


settings = Config()
