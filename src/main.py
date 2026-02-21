from fastapi import FastAPI, Query
from ModelName import ModelName
from Item import Item
from typing import Annotated
import random
from pydantic import AfterValidator


app = FastAPI()
fake_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}

def check_valid_id(id: str):
    if not id.startswith(('isbn-', 'imdb-')):
        raise ValueError('Invalid ID format, it must start with "isbn-" or "imdb-"')
    return id

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

# @app.get("/items/")
# async def read_db_item(skip: int = 0, limit: int = 10):
#     return fake_db[skip: skip + limit]

# @app.get("/items/")
# async def read_items(q: Annotated[str | None, Query(max_length=50, min_length=3)] = 'fixedquery'):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q}) # type: ignore -- python dict has update method
#     return results

# @app.get("/items/")
# async def read_items(q: Annotated[list[str] | None, Query(title="Query String")] = None):
#     query_items = {"q": q}
#     return query_items

@app.get("/items/")
async def read_items(id: Annotated[str | None, AfterValidator(check_valid_id)] = None):
    if id:
        item = data.get(id)
    else:
        id, item = random.choice(list(data.items()))
    return {"id": id, "name": item}

@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    else:
        return {"item_id": item_id}

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    elif model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    else:
        return {"model_name": model_name, "message": "Have some residuals"}
    
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id: int, item_id: str, q: str | None = None, short: bool = False):
    item = {'item_id': item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "this is a short item with a long description"})
    return item

@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.model_dump()}