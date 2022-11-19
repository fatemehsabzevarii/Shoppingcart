from anyio import value


from shopping.product.get_product import *






class Cart:


    @classmethod
    def add_to_cart(cls, **kwargs):
        user_id = kwargs['user_id']
        # check if cart already exists
        for user_carts in Cart:
            data = user_carts.items()
            if int(data['user_id']) == user_id and int(data['product_id']) == kwargs['product_id']:
                return True


    @classmethod
    def carts(cls, user_id):
        result = []
        for user_carts in Cart:
            data = {user_carts.items()}
            result.append(data)
        return result

    @classmethod
    def delete_cart(cls, user_id, rowId):
        # if return 1 is true and return 0 is false it's mean data doesn't exists
        return Cart.delete(f"carts:{user_id}:{rowId}")

    @classmethod
    def delete_all_carts(cls, user_id):
        pass