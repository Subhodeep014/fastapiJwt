from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id:int
    owner_email : EmailStr

    class config:
        from_attributes = True
class TodoBase(BaseModel):
    title:str
    completed : bool=False
class TodoCreate(TodoBase):
    pass
class TodoUpdate(TodoBase):
    pass
class TodoResponse(BaseModel):
    id :int
    owner_email:EmailStr
    title: str
    completed : bool
    class Config:
        from_attributes = True
