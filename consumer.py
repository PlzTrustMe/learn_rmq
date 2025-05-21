import logging
import time
from typing import TYPE_CHECKING

from config import MQ_QUEUE, configure_logging, get_connection

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel
    from pika.spec import Basic, BasicProperties

logger = logging.getLogger(__name__)


def consuming_process(
    channel: "BlockingChannel",
    method: "Basic.Deliver",
    properties: "BasicProperties",
    body: bytes
):
    logger.info("[ ] Start processing message (expensive task!) %r", body)
    start_time = time.time()

    time.sleep(2)

    end_time = time.time()
    logger.info("Finished processing message %r, sending ack!", body)
    channel.basic_ack(delivery_tag=method.delivery_tag)
    logger.warning(
        "[X] Finished in %.2fs processing message %r",
        end_time - start_time,
        body,
    )


def consume_message(channel: "BlockingChannel") -> None:
    channel.basic_consume(
        queue=MQ_QUEUE,
        on_message_callback=consuming_process
    )
    logger.info("Waiting for message...")
    channel.start_consuming()


def main() -> None:
    configure_logging()

    with get_connection() as connection:
        logger.info("Created connection: %s", connection)
        with connection.channel() as channel:
            logger.info("Created channel: %s", channel)
            consume_message(channel)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log.warning("Bye!")
