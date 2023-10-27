from fastapi import FastAPI, Depends, Query
from fastapi.security import OAuth2PasswordBearer
from typing_extensions import Annotated
from typing import Union

app = FastAPI()

# Define an OAuth2PasswordBearer security scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def common_parameters(q: Union[str, None] = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons


@app.get("/users/")
def read_users(commons: dict = Depends(common_parameters)):
    return commons


@app.get("/users_2/")
def read_users_2(commons: dict = {"q": None, "skip": 1, "limit": 100}):
    print("here's users_2 commons:", commons)
    return commons


@app.get("/items_2/")
def read_items_2(q: Annotated[Union[str, None], Query(max_length=50)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


def hello():
    return "world"


def common_parameters_3(
    q: Union[str, None] = None,
    skip: int = 0,
    limit: int = 100,
    blah: str = Depends(hello),
):
    return {"q": q, "skip": skip, "limit": limit, "hello": blah}


@app.get("/users_3/")
def read_users_3(commons: dict = Depends(common_parameters_3)):
    return commons


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


class CommonQueryParams:
    def __init__(
        self,
        item_id: int,
        q: Union[str, None] = None,
        skip: int = 0,
        limit: int = 100
    ):
        self.q = q
        self.skip = skip
        self.limit = limit
        self.item_id = item_id


@app.get("/items_4/{item_id}")
def read_items(commons: CommonQueryParams = Depends(CommonQueryParams)):
    response = {}
    print(commons.item_id)
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip:commons.skip + commons.limit]
    response.update({"items": items})
    return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
