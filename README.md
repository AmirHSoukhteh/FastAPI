# FastAPI
This repository used for learning fast-api

## Install and use FastAPI
### Virtual Environment
```bash
# python -m venv <name of folder>

# linux
python3 -m venv env

# activation
source env/bin/activate
```

### Install
> **Note**
>
> When you install with `pip install "fastapi[standard]"` it comes with some default optional standard dependencies, including `fastapi-cloud-cli`, which allows you to deploy to FastAPI Cloud 😊.
>
> If you don't want to have those optional dependencies, you can instead install `pip install fastapi`.
>
> If you want to install the standard dependencies but without the `fastapi-cloud-cli`, you can install with `pip install "fastapi[standard-no-fastapi-cloud-cli]"`.
```bash
pip install "fastapi[standard]"
```

### First step
```bash

# Project Tree
```bash
.
├── core
│   └── main.py
├── docs
├── LICENSE
├── README.md
└── requirements.txt

```

```py
# main.py

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def hello_world():
    return {"message": "Hello World"}
```
```bash
fastapi dev 
# or 
fastapi dev main.py
```

WE need to work with CRUD requests in first step:
+ C = Creation -> POST
+ R = Read -> GET
+ U = Update -> PATCH/PUT
+ D = Delete -> DELETE

Our sample database is:
```python
# main.py
from fastapi import FastAPI, Query, status, HTTPException, Path, Body
from fastapi.responses import JSONResponse
import random

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app:FastAPI):

    print("Application startup")
    yield
    print("Application shutdown")

app = FastAPI(lifespan=lifespan)

names_list = [
    {"id":1, "name":"ali"},
    {"id":2, "name":"amir"},
    {"id":3, "name":"bahram"},
    {"id":4, "name":"cohon"},
    {"id":5, "name":"dani"},
    {"id":6, "name":"ebrahim"},
]
```
>**PATH:** /names 
> + GET( RETRIEVE),
> + POST( CREATE)
>
> GET 
> ```py
> @app.get("/names")
> async def retrieve_names_list(
>     q : str | None = Query(
>         alias="search",
>         description="It will search with title you provided",
>         example="ali",
>         default=None, 
>         max_length=50
>     )
> ):
>     result = names_list
>     if q:
>         result =  [item for item in names_list if q in item["name"]]
>     return JSONResponse(content=result, status_code=status.HTTP_200_OK)
> 
> ```
>
> POST
>
> ```py
> @app.post("/names")
> async def create_name(
>     name:str | None = Body(
>         embed=True,    
>     )
> ):
>     name_obj = {"id": random.randint(6, 100), "name": name}
>     names_list.append(name_obj)
>     return JSONResponse(content=name_obj, status_code=status.HTTP_201_CREATED)
> ```

> **PATH:** /names/:id 
>+ GET( RETRIEVE), 
>+ PUT/PATCH( UPDATE),
>+ DELETE
>
> GET
>
> ```py
> @app.get("/names/{name_id}")
> async def retrieve_name_detail(
>     name_id:int = Path
>     (
>         title="object id",
>         description="the id of name in names_list",
>         ge=1,
>         example=5
>     )
> ):
>     for name in names_list:
>         if name["id"] == name_id:
>             return JSONResponse(content=name, status_code=status.HTTP_200_OK)
>     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="object didn't find.") 
> ```
>
> PUT
> 
> ```py
> @app.put("/names/{name_id}")
> async def update_name_detail(
>     name_id:int = Path
>     (
>         title="object id",
>         description="the id of name in names_list",
>         ge=1,
>         example=5
>     ),
>     name:str | None = Body(
>         embed=True,    
>     )
> ):
>     for item in names_list:
>         if item["id"] == name_id:
>             item["name"] = name
>             return JSONResponse(content=item, status_code=status.HTTP_200_OK)
>     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="object didn't find.") 
> ```
>
> DELETE
> 
> ```py
> @app.delete("/names/{name_id}")
> async def delete_name(
>     name_id:int = Path
>     (
>         title="object id",
>         description="the id of name in names_list",
>         ge=1,
>         example=5
>     )
> ):
>     for item in names_list:
>         if item["id"] == name_id:
>             names_list.remove(item)
>             return JSONResponse(content={"detail": "object delete successfully."}, status_code=status.HTTP_204_NO_CONTENT)
>     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="object didn't find.") 
> 
> ```

