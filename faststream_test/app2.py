from faststream import FastStream, Logger
from faststream.rabbit import RabbitBroker

from config import CONNECTION_URI
from data import SomeBrokerData
from event import UserCreated

broker = RabbitBroker(CONNECTION_URI)
app = FastStream(broker)


@broker.subscriber("final-queue")
async def handle_msg_from_final_queue(
    data: SomeBrokerData,
    logger: Logger
) -> None:
    logger.info("Final result %s", data)


@broker.subscriber("user-created")
async def handle_msg_from_user_created_queue(
    data: UserCreated,
    logger: Logger
):
    logger.info("Handled %s", data)
