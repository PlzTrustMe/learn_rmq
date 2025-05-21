import logging
import time
from typing import TYPE_CHECKING

from config import (
    MQ_EXCHANGE,
    MQ_QUEUE,
    configure_logging, get_connection,

)

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel


def produce_message(channel: "BlockingChannel") -> None:
    queue = channel.queue_declare(queue=MQ_QUEUE)
    logger.info("Declare queue %r %s", MQ_QUEUE, queue)

    new_message = f"Hello, world from {time.time()}"
    logger.info("Publish new message %s", new_message)

    channel.basic_publish(
        exchange=MQ_EXCHANGE,
        routing_key=MQ_QUEUE,
        body=new_message
    )


def main() -> None:
    configure_logging()

    with get_connection() as connection:
        logger.info("Created connection: %s", connection)
        with connection.channel() as channel:
            logger.info("Created channel: %s", channel)
            produce_message(channel)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.warning("Bye!")
