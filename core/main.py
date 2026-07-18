from fastapi import FastAPI, Query, status, HTTPException, Path, Body
from fastapi.responses import JSONResponse
import random
from schema import PersonCreateSchema, PersonRespondSchema, PersonUpdateSchema
from typing import List

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

# /names (GET(RETRIEVE), POST(CREATE))
@app.get("/names", response_model=List[PersonRespondSchema])
async def retrieve_names_list(
    q : str | None = Query(
        alias="search",
        description="It will search with title you provided",
        example="ali",
        default=None, 
        max_length=50
    )
):
    result = names_list
    if q:
        result =  [item for item in names_list if q in item["name"]]
    return JSONResponse(content=result, status_code=status.HTTP_200_OK)

@app.post("/names", response_model=PersonRespondSchema)
async def create_name(person:PersonCreateSchema):
    name_obj = {"id": random.randint(6, 100), "name": person.name}
    names_list.append(name_obj)
    return JSONResponse(content=name_obj, status_code=status.HTTP_201_CREATED)

# /names/:id (GET(RETRIEVE), PUT/PATCH(UPDATE), DELETE)
@app.get("/names/{name_id}", response_model=PersonRespondSchema)
async def retrieve_name_detail(
    name_id:int = Path
    (
        title="object id",
        description="the id of name in names_list",
        ge=1,
        example=5
    )
):
    for name in names_list:
        if name["id"] == name_id:
            return JSONResponse(content=name, status_code=status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="object didn't find.") 

@app.put("/names/{name_id}", response_model=PersonRespondSchema)
async def update_name_detail(
    person : PersonUpdateSchema,
    name_id:int = Path
    (
        title="object id",
        description="the id of name in names_list",
        ge=1,
        example=5
    ),
    
):
    for item in names_list:
        if item["id"] == name_id:
            item["name"] = person.name
            return JSONResponse(content=item, status_code=status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="object didn't find.") 

@app.delete("/names/{name_id}")
async def delete_name(
    name_id:int = Path
    (
        title="object id",
        description="the id of name in names_list",
        ge=1,
        example=5
    )
):
    for item in names_list:
        if item["id"] == name_id:
            names_list.remove(item)
            return JSONResponse(content={"detail": "object delete successfully."}, status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="object didn't find.") 

@app.get("/")
async def root():
    return JSONResponse(content={"message": "Hello World!"}, status_code=status.HTTP_200_OK)

