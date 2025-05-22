import asyncio

from faststream.rabbit import RabbitBroker

from config import CONNECTION_URI
from data import SomeBrokerData


async def send_message(broker: RabbitBroker) -> None:
    usernames = ["John", "Alice", "Tom", "Jack", "Tommy", "Fred", "Janna",
                 "Kayn", "Elisa", "Kenny"]

    messages = [
        SomeBrokerData(username=username, message=f"Hello from {username}") for
        username in usernames]

    for message in messages:
        await broker.publish(message, queue="test-queue")


async def main() -> None:
    async with RabbitBroker(CONNECTION_URI) as broker:
        await send_message(broker)


if __name__ == "__main__":
    asyncio.run(main())
