from pydantic.types import List
from starlette.requests import Request
from fastapi.security import OAuth2PasswordRequestForm
from shopping.customer.register.models.model_register import Customer
from fastapi import APIRouter, HTTPException, Depends, status, BackgroundTasks
from shopping.customer.register import get_register
from shopping.customer.register.models.schemas import customer_validation
from shopping.customer.register.modules.hash_password import *
from shopping.helper.connection import Db
from typing import List




router = APIRouter(
    tags=[' Customers'],

)


@router.get("/users/", response_model=List[Customer], dependencies=[Depends(Db)])
async def read_users(skip: int = 0, limit: int = 100):
    Customers = cruds.get_users(skip=skip, limit=limit)
    return Customers


@router.delete('/user/{user_id}')
async def delete_customer(user_id: int):
    user = models.User.filter(models.User.id == user_id).first()
    if user:
        user.delete_instance()
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={"message": "User delete."})
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "User not found."})


@router.post('/token', dependencies=[Depends])
def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid phonenumber or password'
        )
    user = {
        'id': user.id,
        'phonenumber': user.phonenumber,

    }
    token = jwt.encode(user, settings.JWT_SECRET)
    return {'access_token': token, 'token_type': 'bearer'}



@router.post('/token', dependencies=[Depends])
def register(data: dict):
    value = Request(**data)
    customer = Customer(phone_number=value.customer_phone_number)
    customer_data = customer.get_customer()
    is_exists_phone_number = customer_data.get("PhoneNumber")


    if is_exists_phone_number:
        message = {
            "hasRegistered": True,
            "message": "شما قبلا ثبت نام کرده اید.",
            "redirect": "login"
        }
        return {"success": False, "error": message, "status_code": 308}
    else:
        if value.customer_password != value.customer_verify_password:
            return {"success": False, "error": "رمز عبور و تکرار آن با هم برابر نیستند.", "status_code": 422}
        customer.set_data(
            customer_phone_number=value.customer_phone_number,
            customer_first_name=value.customer_first_name,
            customer_last_name=value.customer_last_name,
            customer_password=hash_pass(value.customer_password)
        )
        if customer.save():
            customer_id = customer.get_customer().get("customerID")
            message = {
                "message": "ثبت نام شما با موفقیت انجام شد",
                "data": {
                    "customerID": customer_id,
                    "customerIsActive": False
                }
            }
            return {"success": True, "message": message, "status_code": 201}
        else:
            message = {"error": "خطایی در روند ثبت نام رخ داده است لطفا دوباره امتحان کنید"}
            return {"success": False, "error": message, "status_code": 417}



