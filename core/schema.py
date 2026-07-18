from pydantic import BaseModel, field_validator

class BasePersonSchema(BaseModel):
    name : str

    @field_validator
    def validate_name(cls, value):
        if len(value > 32):
            raise ValueError("Name must not exceed 32 character")
        if not value.isalpha():
            raise ValueError("Name must contain only alphabetic character")        
        return value

class PersonCreateSchema(BasePersonSchema):
    pass

class PersonRespondSchema(BasePersonSchema):
    id : int

class PersonUpdateSchema(BasePersonSchema):
    pass
