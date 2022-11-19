import re
from marshmallow import Schema, fields, post_load, validates_schema, ValidationError, RAISE
from pydantic.main import BaseModel

SKIP_VALUES = {"requestType": "", "step": ""}


class CustomFieldsValidation:
    @staticmethod
    def check_phone_number(phone_number: int or None):
        pattern = r"^09[0|1|2|3|4|5|6|7|8|9][0-9]{8}$"
        match = re.fullmatch(pattern, phone_number)
        try:
            phone_number = int(phone_number)
        except ValueError:
            raise ValueError("phone Number must be all digits")
        if len(phone_number) != 11:
            raise ValueError("phone Number must be 11 digits")
        if not match:
            raise ValueError("phone Number is not real")

    @staticmethod
    def check_password(password: str or None):
        if not any(char.islower() for char in password):
            return ValidationError("Password should have at least one lowercase letter")
        if len(password) < 8:
            return ValidationError("Password length should be at least 8")
        if len(password) > 50:
            return ValidationError("Password length should not be greater than 50")
        if not any(char.isdigit() for char in password):
            return ValidationError("Password should have at least one numeral")
        if not any(char.isupper() for char in password):
            return ValidationError("Password should have at least one uppercase letter")


    @staticmethod
    def check_string(string: str or None):
        if len(string) < 4 or len(string) > 80:
            raise ValueError("string length must be between 4 and 100 characters")
        return string






class UserBase(BaseModel):
    phoneNumber: str


class UserCreate(UserBase):
    password: str
    phonenumber : int


class User(UserBase):
    id: int
    is_active: bool


class CustomerSchema(Schema):
    customerID = fields.Int(required=False)
    createdDate = fields.DateTime(required=False)
    phoneNumber = fields.Str(required=False)
    userName = fields.Str(required=False)
    password = fields.Str(required=False)
    firstname = fields.Str(required=False)
    lastname = fields.Str(required=False)




    @validates_schema
    def validate_phone_number(self, data):
        try:
            return CustomFieldsValidation.check_phone_number(data.get("phoneNumber"))
        except Exception as e:
            raise ValidationError({"message": e})

    @validates_schema
    def validate_password(self, data):
        try:
            return CustomFieldsValidation.check_password(data.get("password"))
        except Exception as e:
            raise ValidationError({"message": e})

    @validates_schema
    def validate_email(self, data):
        try:
            return CustomFieldsValidation.check_email(data.get("email"))
        except Exception as e:
            raise ValidationError({"message": e})

    @validates_schema
    def validate_username(self, data):
        try:
            return CustomFieldsValidation.check_string(data.get("userName"))
        except Exception as e:
            raise ValidationError({"message": e})

    @validates_schema
    def validate_first_name(self, data):
        try:
            return CustomFieldsValidation.check_string(data.get("firstname"))
        except Exception as e:
            raise ValidationError({"message": e})

    @validates_schema
    def validate_last_name(self, data):
        try:
            return CustomFieldsValidation.check_string(data.get("lastname"))
        except Exception as e:
            raise ValidationError({"message": e})



