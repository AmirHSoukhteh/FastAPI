from fastapi import FastAPI, Query, status, HTTPException
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
@app.get("/names", status_code=status.HTTP_200_OK)
async def retrieve_names_list(q : str | None = Query(default=None, max_length=50)):
    if q:
        return [item for item in names_list if q in item["name"]]
    return names_list

@app.post("/names")
async def create_name(name:str, status_code=status.HTTP_201_CREATED):
    name_obj = {"id": random.randint(6, 100), "name": name}
    names_list.append(name_obj)
    return name_obj

# /names/:id (GET(RETRIEVE), PUT/PATCH(UPDATE), DELETE)
@app.get("/names/{name_id}", status_code=status.HTTP_200_OK)
async def retrieve_name_detail(name_id:int):
    for name in names_list:
        if name["id"] == name_id:
            return name
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="object didn't find.") 

@app.put("/names/{name_id}", status_code=status.HTTP_200_OK)
async def update_name_detail(name_id:int, name:str):
    for item in names_list:
        if item["id"] == name_id:
            item["name"] = name
            return item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="object didn't find.") 

@app.delete("/names/{name_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_name(name_id:int):
    for item in names_list:
        if item["id"] == name_id:
            names_list.remove(item)
            return {"detail": "object delete successfully."}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="object didn't find.") 

@app.get("/")
async def root():
    return {"message": "Hello World!"}

