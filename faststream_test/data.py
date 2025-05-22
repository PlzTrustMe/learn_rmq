from pydantic import BaseModel


class SomeBrokerData(BaseModel):
    username: str
    message: str
