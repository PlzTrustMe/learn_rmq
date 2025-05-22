import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar, Protocol, Type

from adaptix import Retort
from faststream.rabbit import RabbitBroker

from config import CONNECTION_URI


@dataclass(frozen=True)
class Event(ABC):
    pass


@dataclass(frozen=True)
class UserCreated(Event):
    user_id: int


class EventEmitter(Protocol):
    @abstractmethod
    async def publish(self, event: Event) -> None:
        raise NotImplementedError


class FastStreamEventEmitter(EventEmitter):
    _events_map: ClassVar[dict[Type[Event], str]] = {
        UserCreated: "user-created"
    }

    async def publish(self, event: Event) -> None:
        queue = self._events_map.get(type(event))

        retort = Retort()
        async with RabbitBroker(CONNECTION_URI) as broker:
            await broker.publish(
                retort.dump(event),
                queue=queue
            )


async def main() -> None:
    emitter = FastStreamEventEmitter()

    await emitter.publish(UserCreated(user_id=543))


if __name__ == "__main__":
    asyncio.run(main())
