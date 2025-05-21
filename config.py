import logging

import pika

MQ_HOST = "0.0.0.0"
MQ_PORT = 5672
MQ_USER = "guest"
MQ_PASSWORD = "guest"

MQ_EXCHANGE = ""
MQ_QUEUE = "topic"


def get_connection() -> pika.BlockingConnection:
    return pika.BlockingConnection(
        parameters=pika.ConnectionParameters(
            host=MQ_HOST,
            port=MQ_PORT,
            credentials=pika.PlainCredentials(MQ_USER, MQ_PASSWORD)
        )
    )


def configure_logging(level: int = logging.INFO):
    logging.basicConfig(
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)03d] %(funcName)20s %(module)s:%(lineno)d %(levelname)-8s - %(message)s",
    )
