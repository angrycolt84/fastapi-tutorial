from fastapi import FastAPI, Path, Query, Body, Cookie, Request, Header, Response, File, Form, UploadFile, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse, PlainTextResponse
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from starlette.exceptions import HTTPException as StarletteHTTPException
from ModelName import ModelName
from unicornexception import UnicornException
from Item import Item
from typing import Annotated, Any
from User import User
import datetime as dt
from cookies import Cookies
from Image import Image
from baseuser import UserIn, BaseUser
from offer import Offer
from commonheaders import CommonHeaders
from uuid import UUID
import random
from pydantic import AfterValidator
from FilterParams import FilterParams

app = FastAPI()

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"OMG! An HTTP Error: {repr(exc)}")
    return await http_exception_handler(request, exc)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"OMG! The client sent invalid data: {exc}")
    return await request_validation_exception_handler(request, exc)


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code = 418,
        content = {"message": f"Ooops! {exc.name} did something. There goes a rainbow."}
    )

# @app.exception_handler(StarletteHTTPException)
# async def http_exception_handler(request, exc):
#     return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request, exc: RequestValidationError):
#     message = "Validation Errors: "
#     for error in exc.errors():
#         message = f"\nField: {error['loc']}, Error: {error['msg']}"
#     return PlainTextResponse(message, status_code=400)


fake_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}


def check_valid_id(id: str):
    if not id.startswith(("isbn-", "imdb-")):
        raise ValueError('Invalid ID format, it must start with "isbn-" or "imdb-"')
    return id


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/unicorns/{name}", deprecated=True)
async def read_unicorn(name: str):
    if name == 'yolo':
        raise UnicornException(name=name)
    return {"unicorn_name": name}

@app.get("/portal/")
async def get_portal(teleport: bool = False) -> Response:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    else:
        return JSONResponse(content={"message": "Here's your interdimensional response."})

@app.post("/user/", response_model=BaseUser, summary="Create a user", description="Create a user with all the info")
async def create_user(user: UserIn) -> Any:
    return user

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


# @app.get("/items/")
# async def read_items(id: Annotated[str | None, AfterValidator(check_valid_id)] = None):
#     if id:
#         item = data.get(id)
#     else:
#         id, item = random.choice(list(data.items()))
#     return {"id": id, "name": item}


# @app.get("/items/")
# async def read_items(filter_query: Annotated[FilterParams, Query()]):
#     return filter_query

# @app.get("/items/")
# async def read_items(ads_id: Annotated[str | None, Cookie()] = None):
#     return {"ads_id": ads_id}

# @app.get("/items/")
# async def read_items(user_agent: Annotated[str | None, Header()] = None):
#     return {"User-Agent": user_agent}

# @app.get("/items/")
# async def read_items(x_token: Annotated[list[str] | None, Header()] = None):
#     return {"X-token Values": x_token}

# @app.get("/items/")
# async def read_items(cookies: Annotated[Cookies, Cookie()]):
#     return cookies

# @app.get("/items/")
# async def read_items(headers: Annotated[CommonHeaders, Header()]):
#     return headers

@app.get("/items/", response_model=list[Item])
async def read_items() -> Any:
    return [
        {"name": "Portal Gun", "price": 42.0},
        {"name": "Plumbus", "price": 32.0},
    ]

# @app.get("/items/{item_id}")
# async def read_item(item_id: str, q: str | None = None):
#     if q:
#         return {"item_id": item_id, "q": q}
#     else:
#         return {"item_id": item_id}


# @app.get("/items/{item_id}")
# async def read_item(
#     item_id: Annotated[int, Path(title="The ID of the item to get", gt=0, le=1000)],
#     q: Annotated[str | None, Query(alias="item-query")] = None,
# ):
#     results = {"item_id": item_id}
#     if q:
#         results.update({"q": q})  # type: ignore
#     return results

items = {"foo": "Foo Wrestlers"}

# @app.get("/items/{item_id}")
# async def read_item(
#     item_id: str
# ):
#     if item_id not in items:
#         raise HTTPException(status_code=404, detail="Item not found", headers={"X-Error": "There goes my error"})
#     return {"item": items[item_id]}

@app.get("/items/{item_id}")
async def read_item(
    item_id: int
):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope, I don't like 3.")
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

@app.post("/files/")
async def create_file(
    file: Annotated[bytes, File()],
    fileb: Annotated[UploadFile, File()],
    token: Annotated[str, Form()]
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "this is a short item with a long description"})
    return item


# @app.post("/items/")
# async def create_item(item: Item):
#     item_dict = item.model_dump()
#     if item.tax is not None:
#         price_with_tax = item.price + item.tax
#         item_dict.update({"price_with_tax": price_with_tax})
#     return item_dict


@app.post("/items/")
async def create_item(item: Item) -> Item:
    return item


# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     return {"item_id": item_id, **item.model_dump()}


# @app.put("/items/{item_id}")
# async def update_item(
#     item_id: Annotated[int, Path(title="ID of the item", ge=0, le=1000)],
#     q: str | None = None,
#     item: Item | None = None,
# ):
#     results = {"item_id": item_id}
#     if q:
#         results.update({"q": q}) # type:ignore
#     if item:
#         results.update({"item": item}) # type:ignore
#     return item


# @app.put("/items/{item_id}")
# async def update_item(
#     item_id: Annotated[int, Path(title="ID of item", ge=0, le=1000)],
#     item: Item,
#     user: User,
#     importance: Annotated[int, Body(gt=0)],
#     q: str | None = None
# ):
#     results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
#     if q:
#         results.update({"q": q})
#     return results


@app.put("/items/{item_id}")
async def read_item_new(
    item_id: UUID,
    start_datetime: Annotated[dt.datetime, Body()], 
    end_datetime: Annotated[dt.datetime, Body()],
    process_after: Annotated[dt.timedelta, Body()],
    repeat_at: Annotated[dt.time | None, Body()] = None
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "process_after": process_after,
        "repeat_at": repeat_at,
        "start_process": start_process,
        "duration": duration,
    }

@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer


@app.post("/images/multiple")
async def create_multiple_images(images: list[Image]):
    return images