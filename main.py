import re
import sys
import os
from enum import Enum
from typing import Optional

from fastapi import responses
from fastapi.responses import JSONResponse as j_response
from pydantic import BaseModel, validator, ValidationError
from fastapi import status
from fastapi import FastAPI, HTTPException

from shopping.customer.login import authentication

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

tags = [
    {
        "name": "register",
        "description": "Register "
    },
{
        "name": "Carts",
        "description": "Add to cart, Get, Clear, delete item from cart",
    },
{
        "name": "Products",
        "description": "GET list and by id from db."
    },
{
        "name": "Orders",
        "description": "List order and Create order."
    },
]

app = FastAPI(
    title="ShoppingCart API",
    description="""
         A service for handling and explicit representation of the properties of shopping online.
     """,
    version="0.0.1",
    openapi_tags=tags,
    docs_url="/api/v1/docs"
)


app.include_router(router=customer_router, prefix="/api/v1/carts", tags=["Customer"])

app.include_router(router=products_routers, prefix="/api/v1/products", tags=["Products"])
app.include_router(router=orders_routers, prefix="/api/v1/orders", tags=["Orders"])

app.include_router(router=carts_router, prefix="/api/v1/carts", tags=["Carts"])















class LoginModel(BaseModel):
    mobileNumber: str
    password: str

    @validator('password')
    def validate_password(cls, password) -> bool:
        try:
            if len(password) < 8:
                raise ValueError("Password length should be at least 8")
            if len(password) > 25:
                raise ValueError("Password length should not be greater than 25")
            if not any(char.isdigit() for char in password):
                raise ValueError("Password should have at least one numeral")
            if not any(char.isupper() for char in password):
                raise ValueError("Password should have at least one uppercase letter ")
            if not any(char.islower() for char in password):
                raise ValueError("Password should have at least one  lowercase letter")
            return password
        except Exception as e:
            raise ValidationError(e)

    @validator('mobileNumber')
    def validate_user(cls, mobileNumber):
        try:
            # phone number
            if mobileNumber.isdigit():
                pattern: str = r"^09[0|1|2|3|4|5|6|7|8|9][0-9]{8}$"

                match = re.fullmatch(pattern, mobileNumber)
                if match:
                    return mobileNumber
                else:
                    raise ValueError("not match")
        except Exception as e:
            raise ValidationError(e)


@app.post('/login/')
def user_login(data: LoginModel):
    # user_value = data.user[0]
    # user_type = data.user[1]
    mobileNumber = data.mobileNumber
    password = data.password
    customer = Customer.login(mobileNumber, password)
    if customer:
        # user = authentication.authenticate_user(form_data.mobileNumber, form_data.password)
        access_token = authentication.create_access_token(mobileNumber)
        return j_response(headers=access_token)



    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect mobileNumber or password",
            headers={"token": "Bearer"},
        )


