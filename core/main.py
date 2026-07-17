from fastapi import FastAPI, Query, status, HTTPException, Path
from fastapi.responses import JSONResponse
import random
app = FastAPI()

names_list = [
    {"id":1, "name":"ali"},
    {"id":2, "name":"amir"},
    {"id":3, "name":"bahram"},
    {"id":4, "name":"cohon"},
    {"id":5, "name":"dani"},
    {"id":6, "name":"ebrahim"},
]

# /names (GET(RETRIEVE), POST(CREATE))
@app.get("/names")
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

@app.post("/names")
async def create_name(name:str):
    name_obj = {"id": random.randint(6, 100), "name": name}
    names_list.append(name_obj)
    return JSONResponse(content=name_obj, status_code=status.HTTP_201_CREATED)

# /names/:id (GET(RETRIEVE), PUT/PATCH(UPDATE), DELETE)
@app.get("/names/{name_id}")
async def retrieve_name_detail(
    name_id:int = Path
    (
        alias="object_id",
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

@app.put("/names/{name_id}")
async def update_name_detail(name_id:int, name:str):
    for item in names_list:
        if item["id"] == name_id:
            item["name"] = name
            return JSONResponse(content=item, status_code=status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="object didn't find.") 

@app.delete("/names/{name_id}")
async def delete_name(name_id:int):
    for item in names_list:
        if item["id"] == name_id:
            names_list.remove(item)
            return JSONResponse(content={"detail": "object delete successfully."}, status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="object didn't find.") 

@app.get("/")
async def root():
    return JSONResponse(content={"message": "Hello World!"}, status_code=status.HTTP_200_OK)

