from datetime import datetime
from pydantic import BaseModel, fields
from shopping.product.product_ import Product
from shopping.customer.register.models.model_register import Customer
from shopping.helper.connection import Db
import datetime


class Order(BaseModel):
    customer = fields.ForeignKeyField(Customer, on_delete='CASCADE')
    price = fields.DecimalField(max_digits=10, decimal_places=4)
    date_= fields.DateTimeField(default=datetime.datetime.now())
    address = fields.TextField()

    class Meta:
        database = Db


class OrderItem(BaseModel):
    order = fields.ForeignKeyField(Order, on_delete='CASCADE')
    product = fields.ForeignKeyField(Product, on_delete='CASCADE')

    class Meta:
        database = Db
