from fastapi import FastAPI, Query, status, HTTPException, Path, Body, Depends
from fastapi.responses import JSONResponse
import random
from schema import PersonCreateSchema, PersonRespondSchema, PersonUpdateSchema
from typing import List
from database import Base, engine, get_db, Person
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app:FastAPI):

    print("Application startup")
    Base.metadata.create_all(bind=engine)
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
@app.get("/names",status_code=status.HTTP_200_OK, response_model=List[PersonRespondSchema])
async def retrieve_names_list(
    q : str | None = Query(
        alias="search",
        description="It will search with title you provided",
        example="ali",
        default=None, 
        max_length=50,
    ),
    db : Session = Depends(get_db)
):
    query = db.query(Person)
    if q:
        query = query.filter_by(name=q)
    result = query.all()

    # result = names_list
    # if q:
    #     result =  [item for item in names_list if q in item["name"]]

    return result

@app.post("/names",status_code=status.HTTP_201_CREATED, response_model=PersonRespondSchema)
async def create_name(
    request:PersonCreateSchema,
    db : Session = Depends(get_db)
):
    # name_obj = {"id": random.randint(6, 100), "name": person.name}
    # names_list.append(name_obj)

    new_person = Person(name = request.name)
    db.add(new_person)
    db.commit()
    db.refresh(new_person)

    return new_person

# /names/:id (GET(RETRIEVE), PUT/PATCH(UPDATE), DELETE)
@app.get("/names/{person_id}", response_model=PersonRespondSchema)
async def retrieve_name_detail(
    person_id:int = Path
    (
        title="object id",
        description="the id of name in names_list",
        ge=1,
        example=5
    ),
    db : Session = Depends(get_db)
):
    person = db.query(Person).filter_by(id=person_id).one_or_none()
    
    if person:
        return person
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="object didn't find.") 

@app.put("/names/{person_id}",status_code=status.HTTP_200_OK, response_model=PersonRespondSchema)
async def update_name_detail(
    request : PersonUpdateSchema,
    person_id:int = Path
    (
        title="object id",
        description="the id of name in names_list",
        ge=1,
        example=5
    ),
    db : Session = Depends(get_db)
):
    person = db.query(Person).filter_by(id=person_id).one_or_none()
    if person:
        person.name = request.name
        db.commit()
        db.refresh(person)
        return person
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="object didn't find.") 

@app.delete("/names/{person_id}")
async def delete_name(
    person_id:int = Path
    (
        title="object id",
        description="the id of name in names_list",
        ge=1,
        example=5
    ),
    db : Session = Depends(get_db)
):
    # for item in names_list:
    #     if item["id"] == person_id:
    #         names_list.remove(item)

    person = db.query(Person).filter_by(id=person_id).one_or_none()
    if person:
        db.delete(person)
        db.commit()
        return JSONResponse(content={"detail": "object delete successfully."}, status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="object didn't find.") 

@app.get("/")
async def root():
    return JSONResponse(content={"message": "Hello World!"}, status_code=status.HTTP_200_OK)

