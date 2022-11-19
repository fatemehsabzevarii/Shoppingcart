from typing import List
from fastapi import APIRouter, Depends
from shopping.helper.connection import Db
from shopping.product.schema.validation_product import *
from shopping.product.get_product import *



router = APIRouter(
    tags=['Products'],
    prefix='/products'
)



@router.get('/list')
def products():
    return get_products()


@router.get('/detail/{product_id}'))
def product(product_id: int):
    return get_product(product_id)
