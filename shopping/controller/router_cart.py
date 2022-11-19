from shopping.customer.login.authentication import *
from starlette.responses import JSONResponse
from fastapi import APIRouter, Depends, status
from shopping.helper.connection import Db
from shopping.cart.schema.validation_cart import *
from shopping.cart.get_cart import Cart
from shopping.product.get_product import *
from ..cart import schema
from ..customer.register.models.model_register import Customer

router = APIRouter(
    tags=['Carts']
)


@router.post('/add', dependencies=[Depends(Db)])
def add_to_cart(add_to_cart: schema.AddToCart):
    product = get_product(add_to_cart.product_id)
    Cart.add_to_cart(
        customer_id = customer.id,
        product_id = product.id,
        product_image = str(product.image),
        product_price = str(product.price * add_to_cart.quantity),
        product_quantity = add_to_cart.quantit)
    content = {'message': 'Add to cart.'}
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)


@router.get('/list')
def carts(customer: Customer ):
    total_price = 0
    items = Cart.carts(customer.id)
    for item in items:
        total_price += float(item['product_price'])

    return {'total_price': total_price, 'items': items}


@router.delete()
def clear_cart(customer: Customer ):
    Cart.delete_all_carts(customer.id)
    content = {'message': 'Clear carts.'}
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=content)


@router.delete('/delete-item-cart/')
def delete_item_cart():
   pass