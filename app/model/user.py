from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional

class UserCreate(BaseModel):
    username : str 
    password: str
    email: EmailStr

class UserLogin(BaseModel):
    email: EmailStr
    password: str