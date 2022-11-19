from fastapi import HTTPException, status
from shopping.product.schema import validation_product
from shopping.product import product_



def get_products():
    return list()


def create_product(name,image,price,):
    db_product = product_.Product( name=name,image=image,price=price)
    db_product.save()

    return db_product




def delete_product(product_id: int):
    product = product_.Product(product_.Product.id == product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found.')
    product.delete()
    return 'Done.'


def get_product(product_id: int):
    product = product_.Product(product_.Product.id == product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found.')
    return product
