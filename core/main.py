from fastapi import FastAPI, Query, status, HTTPException, Path, Body
from fastapi.responses import JSONResponse
from itertools import count

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app:FastAPI):

    print("Application startup")
    yield
    print("Application shutdown")

app = FastAPI(lifespan=lifespan)

costs_list = [
    {"id":1, "description": "tax", "cost": 10},
    {"id":2, "description": "buying new car", "cost": 1000},
    {"id":3, "description": "game, pofak", "cost": 100}
]

# /costs (GET(RETRIEVE), POST(CREATE))
@app.get("/costs")
async def retrieve_costs_list(
    q : str | None = Query(
        alias="search",
        description="It will search with title you provided",
        example="tax",
        default=None, 
        max_length=50
    )
):
    result = costs_list
    if q:
        result =  [item for item in costs_list if q in item["description"]]
    return JSONResponse(content=result, status_code=status.HTTP_200_OK)

id_index = count(start=4)

@app.post("/costs")
async def create_cost(
    description:str | None = Body
    (
        default= "I don't know!",
        description= "Why are you spending this money?"
    ),
    cost:int | None = Body
    (
        default= 0,
        description= "How much money do you spend?"
    ),
):
    cost_obj = {
        "id": next(id_index), 
        "description": description, 
        "cost":cost
        }

    costs_list.append(cost_obj)
    return JSONResponse(content=cost_obj, status_code=status.HTTP_201_CREATED)

# /costs/:id (GET(RETRIEVE), PUT/PATCH(UPDATE), DELETE)
@app.get("/costs/{cost_id}")
async def retrieve_cost_detail(
    cost_id:int = Path
    (
        title="object id",
        description="the id of cost in costs_list",
        ge=1,
        example=5
    )
):
    for element in costs_list:
        if element["id"] == cost_id:
            return JSONResponse(content=element, status_code=status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="object didn't find.") 

@app.put("/costs/{cost_id}")
async def update_cost_detail(
    cost_id:int = Path
    (
        title="object id",
        description="the id of cost in costs_list",
        ge=1,
        example=5
    ),
    description:str | None = Body(),
    cost:int | None = Body()
):
    for item in costs_list:
        if item["id"] == cost_id:
            item["cost"] = cost
            item["description"] = description
            return JSONResponse(content=item, status_code=status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="object didn't find.") 

@app.delete("/costs/{cost_id}")
async def delete_cost(
    cost_id:int = Path
    (
        title="object id",
        description="the id of cost in costs_list",
        ge=1,
        example=5
    )
):
    for item in costs_list:
        if item["id"] == cost_id:
            costs_list.remove(item)
            return JSONResponse(content={"detail": "object delete successfully."}, status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="object didn't find.") 


@app.get("/")
async def root():
    return JSONResponse(content={"message": "Hello World!"}, status_code=status.HTTP_200_OK)

