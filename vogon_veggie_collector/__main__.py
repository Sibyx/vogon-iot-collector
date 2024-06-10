import json
import logging
from typing import TypedDict

from paho.mqtt import subscribe
from psycopg_pool import ConnectionPool

from vogon_veggie_collector.config import Config


class UserData(TypedDict):
    pool: ConnectionPool


class App:
    def __init__(self):
        self._config = Config()

        logging.getLogger().setLevel(self._config.LOG_LEVEL)

        if self._config.VERBOSE:
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(logging.Formatter(
                '[%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d]: %(message)s',
                datefmt='%Y-%m-%dT%H:%M:%S%z'
            ))

        logging.info("Loading VogonVeggieCollector %s", self._config.VERSION)

        self._database_pool = ConnectionPool(conninfo=self._config.DATABASE_URI)

    @staticmethod
    def on_message(client, userdata: UserData, message):
        logging.debug("Topic [%s]: %s" % (message.topic, message.payload))
        payload = json.loads(message.payload.decode())

        with userdata['pool'].connection() as conn:
            with conn.cursor() as cur:
                sql = """
                INSERT INTO measurements (device_address, pressure, temperature, humidity, created_at) VALUES (%s, %s, %s, %s, now());
                """
                cur.execute(sql, (payload['address'], payload['pressure'], payload['temperature'], payload['humidity']))

    def run(self):
        subscribe.callback(
            self.on_message,
            [self._config.MQTT_TOPIC],
            hostname=self._config.MQTT_BROKER,
            userdata={
                "pool": self._database_pool
            }
        )


if __name__ == "__main__":
    app = App()
    app.run()
