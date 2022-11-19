from pydantic import BaseModel, Field
from shopping.helper.connection import Db




class Product(BaseModel):
    name = Field.StringField(required=True, max_length=80)
    image = Field.CharField(required=False, max_length=100, unique=True)
    price = Field.FloatField(required=True, max_digits=10, decimal_places=2)

    @staticmethod
    def get_categories():
        with Db() as mongo:
            result = mongo.category.find({}, {"_id": 0, "products": 0})
            return result.get("category")


    @staticmethod
    def get_products(name):
        with Db() as mongo:
            result = mongo.custom_category.find_one({"name": name}, {"_id": 0})
            if result:
                return result.get("products")
            return None


    @staticmethod
    def save(name):
        with Db() as mongo:
            result = mongo.custom_category.insert_one({"name": name}, {"_id": 0})
            if result:
                return result.get("products")
            return None


    @staticmethod
    def remove_product(name,product: str):
        with Db() as mongo:
            result = mongo.category.update_one({"name": name}, {"$pull": {"products": product}})
            item = mongo.category.find_one(
                {"name": name, "name.$.product_id": {"$regex": "^" + product.get("product_id")}})

            if item.get("products") :
                mongo.category.update_one({"name": name},
                                                 {"$pull": {"products.$.system_code": product.get("product_id")}})
            if result.count:
                return {f'message': f'product removed  successfully'}
            return {'error': 'failed'}





