from pydantic import BaseModel
from typing import  List




class category(BaseModel):
    name:str

class ProductCreate(BaseModel):
    name: str
    image: str
    price: float




class ProductUpdata(BaseModel):
    title: str
    body: str
    price: float




class ProductList(BaseModel):
    id: int



class ProductDetail(BaseModel):
    id: int


