from typing import Optional
from pydantic import BaseModel
import datetime


class Token(BaseModel):
    access_token:str
    token_type: str

class TokenData(BaseModel):
    phoneNumber: Optional[str] = None

class User(BaseModel):
    phoneNumber: str


class UserCreate(User):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.phoneNumber = None
        self.username = None

    password: str
    phoneNumber: str
    username:str

