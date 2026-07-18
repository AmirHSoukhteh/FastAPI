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

# Understanding Python `dataclass` vs. `Pydantic`

## What is `dataclass`?
Introduced in Python 3.7, the `@dataclass` decorator is a powerful tool for modeling data. It automatically generates special methods like `__init__()` (for initialization) and `__repr__()` (for string representation), saving you from writing repetitive boilerplate code.

### Basic Usage
Here is how you can use it to create a simple `User` class:

```python
from dataclasses import dataclass

@dataclass
class User:
    id: int
    name: str
    age: int

# Creating an instance
user = User(id=1, name="Ali", age=30)
print(user)  
# Output: User(id=1, name='Ali', age=30)
```
*Notice how we didn't need to write an `__init__` or `__repr__` method manually!*

---

## `dataclass` vs. `Pydantic`
While `dataclass` is great for simple data structures, **Pydantic** is a robust data validation library. Here are the key differences:

### 1. Data Validation
* **`dataclass`**: It is just a simple data structure. It **does not** validate the data types of the values you pass in.
* **`Pydantic`**: It strictly validates input data against the defined types.

### 2. Type Coercion (Casting)
* **`dataclass`**: Does not convert data types. If you pass a string `"1"` to an `int` field, it just stores it as a string.
* **`Pydantic`**: Automatically coerces (converts) data to the correct type if possible.

**Example: Type Coercion in Pydantic**
```python
from pydantic import BaseModel

class UserModel(BaseModel):
    id: int
    name: str
    age: int

# Notice we are passing strings for id and age
user = UserModel(id="1", name="Ali", age="30")
print(user)  
# Output: id=1 name='Ali' age=30 (Pydantic automatically converted strings to ints!)
```

**Example: No Coercion in `dataclass`**
```python
# Passing strings to a dataclass expecting ints
user = User(id="1", name="Ali", age="30") 
# It won't throw an error immediately, but the types will be wrong (strings instead of ints), 
# which can cause hidden bugs later in your code!
```

### 3. Error Handling
* **`dataclass`**: Fails silently on type mismatches. Python won't complain until you try to use the data incorrectly.
* **`Pydantic`**: Catches invalid inputs immediately and provides clear, detailed error messages.

### 4. JSON and API Compatibility
* **`dataclass`**: Lacks built-in methods for easy JSON serialization.
* **`Pydantic`**: Has built-in methods to easily convert models to and from JSON.

**Example: JSON Serialization**
```python
user = UserModel(id=1, name="Ali", age=30)

# Pydantic makes it easy to dump to JSON
print(user.model_dump_json()) 
# Output: {"id":1,"name":"Ali","age":30}
```
*(Note: If you are using the older Pydantic V1, the method is `.json()`. In modern Pydantic V2, use `.model_dump_json()`)*

---

## Why does FastAPI use Pydantic?
FastAPI relies heavily on Pydantic because building web APIs requires strict and secure data handling. 

**Key advantages of Pydantic in FastAPI:**
1. **Request Validation**: Automatically checks if incoming API requests have the correct data structure.
2. **Automatic Type Conversion**: Converts incoming JSON strings to integers, dates, etc., seamlessly.
3. **Clear Error Messages**: Returns helpful `422 Unprocessable Entity` errors to the client if they send bad data.
4. **API Documentation**: Integrates perfectly with Swagger UI to auto-generate interactive API docs.

---

## Summary
* Use **`dataclass`** when you need a simple, lightweight container for data within your internal application logic.
* Use **`Pydantic`** when you are building APIs (like with FastAPI), handling external user input, or need strict data validation and JSON serialization.

# Comprehensive Guide to Pydantic Models in Python & FastAPI

This guide provides a step-by-step, beginner-friendly overview of using Pydantic for data validation, serialization, and modeling in Python, with a focus on FastAPI integration. 

*(Note: This guide uses **Pydantic V2** syntax, which is the current modern standard.)*

---

## 1. Creating Your First Pydantic Model
To use Pydantic, you start by inheriting from `BaseModel`. This allows you to define the structure and data types of your data.

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None  # Optional field, defaults to None
    price: float
    tax: float | None = None        # Optional field, defaults to None

# Creating an instance (Notice type coercion: strings are converted to float)
item = Item(name="Laptop", description="A great laptop", price="1299.99", tax="0")

print(item)  
# Output: name='Laptop' description='A great laptop' price=1299.99 tax=0.0
```

---

## 2. Using Pydantic Models in FastAPI
Pydantic integrates seamlessly with FastAPI. You can use your models directly as type hints in your route handlers to automatically validate incoming request bodies.

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items/")
async def create_item(item: Item):
    # FastAPI automatically validates the request body against the Item model
    return {"message": "Item created successfully", "item": item}
```
*When a user sends a request to `/items/`, FastAPI will ensure the JSON payload matches the `Item` structure exactly.*

---

## 3. Advanced Data Validation
While basic types (`str`, `int`, `float`) are useful, Pydantic provides specialized types for stricter validation.

### Example: Email Validation
Instead of just accepting any string for an email, you can use `EmailStr` to ensure the input is a valid email format.

```python
from pydantic import BaseModel, EmailStr

class Student(BaseModel):
    name: str
    email: EmailStr  # Will raise an error if the string is not a valid email format

# student = Student(name="Ali", email="invalid-email") # This will raise a ValidationError
student = Student(name="Ali", email="ali@example.com") # This works perfectly
```
*Note: Pydantic also validates types on assignment. If you try to assign a non-numeric string (like `"test"`) to an `int` field, it will raise a `ValidationError`. However, a numeric string like `"12"` will be safely coerced into the integer `12`.*

---

## 4. Validating Data Programmatically
You can validate data before creating an object using `model_validate` (for dictionaries) or `model_validate_json` (for JSON strings).

### Validating a Dictionary
```python
from pydantic import BaseModel, ValidationError

class Person(BaseModel):
    first_name: str
    last_name: str
    age: int

# Successful validation
data = {"first_name": "Ali", "last_name": "Bigdeli", "age": 30}
person = Person.model_validate(data)
print(person)  
# Output: first_name='Ali' last_name='Bigdeli' age=30

# Failed validation (missing 'age')
bad_data = {"first_name": "Ali", "last_name": "Bigdeli"}
try:
    Person.model_validate(bad_data)
except ValidationError as e:
    print("Validation failed!")
    print(e)
    # Output includes: 1 validation error for Person \n age \n Field required [type=missing...]
```

### Validating a JSON String
```python
json_data = '''
{
    "first_name": "Ali",
    "last_name": "Bigdeli",
    "age": 30
}
'''
person = Person.model_validate_json(json_data)
print(person)  
# Output: first_name='Ali' last_name='Bigdeli' age=30
```

---

## 5. Custom Field Validation
Sometimes built-in types aren't enough. You can write custom validation logic using the `@field_validator` decorator.

```python
from pydantic import BaseModel, field_validator
import re

class Student(BaseModel):
    name: str
    
    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        # Ensure the name only contains letters and spaces
        pattern = r'^[a-zA-Z\s]+$'        
        if not re.match(pattern, value):
            raise ValueError("Name cannot contain numbers, special characters, or symbols")
        return value

# student = Student(name="Ali123") # This will raise a ValueError
student = Student(name="Ali Bigdeli") # This passes validation
```

---

## 6. Serialization: Converting Models to Dict/JSON
Pydantic models have built-in methods to convert validated data back into standard Python dictionaries or JSON strings.

```python
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    name: str
    email: EmailStr
    account_id: int

user = User(name="Ali Bigdeli", email="ali@example.com", account_id="123")

# 1. Convert to Dictionary
print(user.model_dump())  
# Output: {'name': 'Ali Bigdeli', 'email': 'ali@example.com', 'account_id': 123}

# 2. Convert to JSON String
print(user.model_dump_json())  
# Output: {"name":"Ali Bigdeli","email":"ali@example.com","account_id":123}

# 3. Pretty-print JSON
print(user.model_dump_json(indent=2))
# Output:
# {
#   "name": "Ali Bigdeli",
#   "email": "ali@example.com",
#   "account_id": 123
# }
```

### FastAPI's `jsonable_encoder`
If you need to convert a Pydantic model into a format ready for a database or a custom JSON response, FastAPI provides `jsonable_encoder`:

```python
from fastapi.encoders import jsonable_encoder

json_compatible_data = jsonable_encoder(user)
print(json_compatible_data) 
# Output: {'name': 'Ali Bigdeli', 'email': 'ali@example.com', 'account_id': 123}
```

---

## 7. Custom Serialization with `@field_serializer`
You can customize how specific fields are formatted when the model is serialized.

```python
from pydantic import BaseModel, field_serializer

class Model(BaseModel):
    number: float

    @field_serializer("number")
    def serialize_float(self, value: float) -> float:
        return round(value, 2)  # Round to 2 decimal places during serialization

m = Model(number=1/3)
print(m.model_dump())  
# Output: {'number': 0.33}
```
*This is especially useful when preparing data to be sent to a frontend, ensuring a consistent and clean format.*

---

## 8. Advanced Field Configurations

### Nullable and Optional Fields
You can make fields optional by providing a default value of `None`. In modern Python, `str | None` is preferred, but `Optional[str]` from the `typing` module works identically.

```python
from typing import Optional
from pydantic import BaseModel

class Person(BaseModel):
    first_name: str
    last_name: str
    age: int = 0                  # Default value
    title: str | None = None      # Nullable field (Optional)

# 'title' and 'age' can be omitted during creation
person = Person(first_name="Ali", last_name="Bigdeli")
```

### List Fields
You can enforce that a field must be a list of a specific type.

```python
from typing import List
from pydantic import BaseModel

class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    access_ids: List[int] = []    # Defaults to an empty list of integers

person = Person(first_name="Ali", last_name="Bigdeli", age=30, access_ids=[1, 2, "3"]) 
# "3" is automatically coerced to the integer 3

person.access_ids.extend([4, 5, 6])
```

### Using `Field` for Customization
The `Field` function allows you to add metadata, constraints, and default behaviors to your model attributes.

```python
from pydantic import BaseModel, Field

class Person(BaseModel):
    first_name: str = Field(min_length=2, max_length=50)
    last_name: str = Field()
    age: int = Field(gt=0, description="Age must be greater than 0")
```

### Field Aliases
Sometimes the JSON key you receive doesn't match Python's naming conventions (e.g., contains spaces). You can use an `alias` to map them.

```python
from pydantic import BaseModel, Field, ConfigDict

class Person(BaseModel):
    # Allow using either the alias OR the actual field name for instantiation
    model_config = ConfigDict(populate_by_name=True)
    
    first_name: str = Field(alias="First Name")
    last_name: str = Field(alias="LastName")
    age: int = Field(alias="Age")

# You can instantiate using the aliases:
data = {"First Name": "Ali", "LastName": "Bigdeli", "Age": 30}
person = Person.model_validate(data)

# ...or the actual field names (because of populate_by_name=True):
person2 = Person(first_name="Ali", last_name="Bigdeli", age=30)

# By default, serialization uses the Python field names:
print(person.model_dump()) 
# Output: {'first_name': 'Ali', 'last_name': 'Bigdeli', 'age': 30}

# To serialize using the aliases, pass by_alias=True:
print(person.model_dump(by_alias=True)) 
# Output: {'First Name': 'Ali', 'LastName': 'Bigdeli', 'Age': 30}
```

### Dynamic Defaults with `default_factory`
If a default value needs to be calculated dynamically (like the current timestamp or a random ID), use `default_factory`.

```python
from pydantic import BaseModel, Field
from datetime import datetime, timezone

class Person(BaseModel):
    first_name: str
    last_name: str
    title: str | None = Field(default=None)
    # Generates a new UTC timestamp every time a new object is created
    created_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

person = Person(first_name="Ali", last_name="Bigdeli")

print(person.model_dump())
# Output: {'first_name': 'Ali', 'last_name': 'Bigdeli', 'title': None, 'created_date': datetime.datetime(...)}

print(person.model_dump_json())
# Output: {"first_name":"Ali","last_name":"Bigdeli","title":null,"created_date":"2024-02-17T18:31:36.995400Z"}
```

---

## 💡 Important Note on Mutability in Pydantic V2
In Pydantic V2, models validate data **on assignment** by default. This means if you try to mutate an attribute with an invalid type after the object is created, Pydantic will catch it and raise a `ValidationError`.

```python
person = Person(first_name="Ali", last_name="Bigdeli", age=30)

# This works (valid type coercion)
person.age = "31"  # age is now safely converted to the integer 31

# This FAILS and raises a ValidationError
# person.age = "thirty" 
```
*This behavior protects your application from silent bugs and ensures data integrity throughout the entire lifecycle of your objects.*
