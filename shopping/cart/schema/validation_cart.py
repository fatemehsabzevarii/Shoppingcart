from pydantic import BaseModel
from typing import Any, List



class AddToCart(BaseModel):
    product_id: int
    quantity: int


class CartItems(BaseModel):
    customer_id: str
    product_id: str
    image: str
    price: str
    quantity: str



class Carts(BaseModel):
    total_price: float
    items: List[CartItems] = []

