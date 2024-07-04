import json
import logging
from typing import TypedDict

from paho.mqtt import subscribe
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

from vogon_iot_collector.config import Config


class UserData(TypedDict):
    pool: ConnectionPool


class App:
    def __init__(self):
        self._config = Config()

        logging.getLogger().setLevel(self._config.LOG_LEVEL)

        if self._config.VERBOSE:
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(logging.Formatter(
                '[%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(line no)d]: %(message)s',
                datefmt='%Y-%m-%dT%H:%M:%S%z'
            ))

        logging.info("Loading Vogon IoT Collector %s", self._config.VERSION)

        self._database_pool = ConnectionPool(conninfo=self._config.DATABASE_URI)

    @staticmethod
    def raw_collector(client, userdata: UserData, message):
        logging.debug("Topic [%s]: %s" % (message.topic, message.payload))
        payload = json.loads(message.payload.decode())

        with userdata['pool'].connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                sql = """
                SELECT parameter_id FROM sensor_parameters WHERE sensor_id = %s AND sensor_value = %s;
                """
                parameter_id = cur.execute(sql, (payload['sensor'], payload['parameter'])).fetchone()['parameter_id']

            with conn.cursor() as cur:
                sql = """
                INSERT INTO measurements (device_address, parameter_id, content) VALUES (%s, %s, %s);
                """
                cur.execute(sql, (payload['address'], parameter_id, payload['value']))

    def run(self):
        subscribe.callback(
            self.raw_collector,
            [
                '+/+/raw',  # {service}/{node}/raw
                '+/+/*/raw',  # {service}/{sink}/{node}/raw
            ],
            hostname=self._config.MQTT_BROKER,
            userdata={
                "pool": self._database_pool
            }
        )


if __name__ == "__main__":
    app = App()
    app.run()
