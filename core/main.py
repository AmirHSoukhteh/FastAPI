from fastapi import FastAPI
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
async def retrieve_names_list():
    return names_list

@app.post("/names")
async def create_name(name:str):
    name_obj = {"id": random.randint(6, 100), "name": name}
    names_list.append(name_obj)
    return name_obj

# /names/:id (GET(RETRIEVE), PUT/PATCH(UPDATE), DELETE)
@app.get("/names/{name_id}")
async def retrieve_name_detail(name_id:int):
    for name in names_list:
        if name["id"] == name_id:
            return name
    return {"detail": "object didn't find."}

@app.put("/names/{name_id}")
async def update_name_detail(name_id:int, name:str):
    for item in names_list:
        if item["id"] == name_id:
            item["name"] = name
            return item
    return {"detail": "object didn't find."}

@app.delete("/names/{name_id}")
async def delete_name(name_id:int):
    for item in names_list:
        if item["id"] == name_id:
            names_list.remove(item)
            return {"detail": "object delete successfully."}
    return {"detail": "object didn't find."}

@app.get("/")
async def root():
    return {"message": "Hello World!"}

