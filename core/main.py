from fastapi import FastAPI, Query, status, HTTPException, Path, Body
from fastapi.responses import JSONResponse
from itertools import count
app = FastAPI()

cost_list = []

# /names (GET(RETRIEVE), POST(CREATE))
@app.get("/costs")
async def retrieve_names_list(
    q : str | None = Query(
        alias="search",
        description="It will search with title you provided",
        example="tax",
        default=None, 
        max_length=50
    )
):
    result = cost_list
    if q:
        result =  [item for item in cost_list if q in item["description"]]
    return JSONResponse(content=result, status_code=status.HTTP_200_OK)

id_index = count(start=1)

@app.post("/costs")
async def create_name(
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

@app.get("/")
async def root():
    return JSONResponse(content={"message": "Hello World!"}, status_code=status.HTTP_200_OK)

