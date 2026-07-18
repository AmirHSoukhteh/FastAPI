from pydantic import BaseModel

class BasePersonSchema(BaseModel):
    name : str

class PersonCreateSchema(BasePersonSchema):
    pass

class PersonRespondSchema(BasePersonSchema):
    id : int

class PersonUpdateSchema(BasePersonSchema):
    pass
