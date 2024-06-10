import os
import tomllib
from pathlib import Path


class Config:
    VERBOSE: bool = os.getenv('VOGON__VERBOSE', '1') == '1'
    LOG_LEVEL: str = os.getenv('VOGON__LOG_LEVEL', 'INFO')
    DATABASE_URI: str = os.getenv('VOGON__DATABASE_URI')
    MQTT_BROKER: str = os.getenv('VOGON__MQTT_BROKER')
    MQTT_TOPIC: str = os.getenv('VOGON__MQTT_TOPIC', '+/+/+')
    BASE_DIR: Path = Path(__file__).resolve(strict=True).parent.parent
    VERSION: str = 'dev'

    def __init__(self):
        with open(self.BASE_DIR / "pyproject.toml", "rb") as f:
            pyproject = tomllib.load(f)
            self.VERSION = pyproject["tool"]["poetry"]["version"]
