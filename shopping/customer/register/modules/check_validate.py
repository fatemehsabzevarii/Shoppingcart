from fastapi import responses, status
from customer.register.models.schema.customer_serialization import CustomFieldsValidation
from customer.register.database.connection import Db
from customer.register.models.customer import Customer


class UniqueFieldsValidation:
    @staticmethod
    def validate_and_unique_mobile_number(mobile_number):
        CustomFieldsValidation.check_mobile_number(mobile_number)
        with Db():
            customer = Customer.objects(mobileNumber=mobile_number)
            if customer:
                raise ValueError("mobile number exists")

    @staticmethod
    def validate_and_unique_username(username):
        CustomFieldsValidation.check_string(username)
        with Db():
            customer = Customer.objects(userName=username)
            if customer:
                raise ValueError("username exists")

    @staticmethod
    def validate_and_unique_email(email):
        validate_email = CustomFieldsValidation.check_email(email)
        if validate_email == email:
            with Db():
                customer = Customer.objects(email=email)
                if customer:
                    return responses.JSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                                  content={"message": "email exists"})
