from pydantic import BaseModel
from Item import Item

class Offer(BaseModel):
    name: str
    description: str
    price: float
    items: list[Item]