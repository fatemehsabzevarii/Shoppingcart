from datetime import datetime
from pydantic import BaseModel, fields


from shopping.helper.connection import Db


class Customer(BaseModel):
    objects = None


first_name = fields.StringField(required=True, max_length=80)
last_name = fields.StringField(required=True, max_length=80)
phone_number = fields. StringField(required=False, min_length=11, max_length=11)
password = fields.FloatField(required=True)


class Meta:
    database = Db

    def save(self):
        if not self.createdDate:
            self.createdDate = datetime.timestamp(datetime.now())
        return super().save()


    @staticmethod
    def login(phoneNumber, password):
        if phoneNumber:
            with Db():
                customer = Customer.objects(phoneNumber=phoneNumber, password=password)
                if customer:
                    return True
                return False