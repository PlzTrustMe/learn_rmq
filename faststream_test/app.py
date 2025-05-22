from faststream import FastStream, Logger
from faststream.rabbit import RabbitBroker

from config import CONNECTION_URI
from data import SomeBrokerData

broker = RabbitBroker(CONNECTION_URI)
app = FastStream(broker)


@broker.subscriber("test-queue")
async def handle_msg_from_test_queue(
    data: SomeBrokerData,
    logger: Logger
) -> None:
    logger.info(f"Получено: {data.username} сказал '{data.message}'")

    processed_msg = SomeBrokerData(
        username=data.username,
        message=data.message.upper()
    )

    await broker.publish(processed_msg, queue="output-queue")
    await broker.publish(processed_msg, queue="final-queue")


@broker.subscriber("output-queue")
async def handle_msg_from_output_queue(
    data: SomeBrokerData,
    logger: Logger
) -> None:
    logger.info(
        f"Промежуточный результат: {data.username} сказал {data.message!r}"
    )
