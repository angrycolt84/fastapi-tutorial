from pydantic import BaseModel, HttpUrl

class Image(BaseModel):
    url: HttpUrl
    name: str