from pydantic import BaseModel,validator
from typing import Optional


class UserRegister(BaseModel):
    name: str
    email: str
    password: str
    role: str
    phone:str
    
    @validator('name','role', 'email','phone','password', pre=True)
    def check_not_empty(cls, v):
        if isinstance(v, str):
            assert v != '', 'Fields are required'
        return v

class Userlogin(BaseModel):
    email: str
    password: str
    
    @validator('email','password', pre=True)
    def check_not_empty(cls, v):
        if isinstance(v, str):
            assert v != '', 'Fields are required'
        return v