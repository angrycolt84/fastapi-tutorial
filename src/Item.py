from pydantic import BaseModel, Field
from Image import Image



class BaseItem(BaseModel):
    description: str
    type: str

class CarItem(BaseItem):
    type: str = "Car"

class PlaneItem(BaseItem):
    type: str = "Plane"
    size: int


class Item(BaseModel):
    name: str = Field(examples=["Foo"])
    description: str | None = Field(default=None, examples=["A Very Nice Item"])
    price: float = Field(examples=[35.4])
    tax: float | None = Field(default=None, examples=[2.75])
    tags: set[str] = set()
    image: list[Image] | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ]
        }
    }