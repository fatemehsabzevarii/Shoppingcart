import re
from typing import Optional

from fastapi import HTTPException, Query
from pydantic import BaseModel, validator, Field



class CustomerPhoneNumber(BaseModel):
    CustomerPhoneNumber: str = Field(
        title="شماره موبایل",
        alias="CustomerPhoneNumber",
        name="CustomerPhoneNumber",
        description="customer phone number",
        dataType="str",
        type="PhoneNumber",
        isRequired=True
    )

class ChangePassword(BaseModel):
    oldPassword: str = Field(
        title="رمز عبور قبلی",
        alias="customerOldPassword",
        name="customerOldPassword",
        placeholder="abcd1234ABCD",
        description="password must be string and len between 8 and 32 character",
        minLength=8,
        maxLength=32,
        dataType="string",
        type="password",
        isRquired=True,
        regexPattern="^^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,32}$",
    )
    newPassword: str = Field(
        title="رمز عبور جدید",
        alias="customerNewPassword",
        name="customerNewPassword",
        placeholder="abcd1234ABCD",
        description="password must be string and len between 8 and 32 character",
        minLength=8,
        maxLength=32,
        dataType="string",
        type="password",
        isRquired=True,
        regexPattern="^^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,32}$",
    )

    @validator("oldPassword", "newPassword")
    def validate_password(cls, code):
        pattern = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,32}$"
        match = re.fullmatch(pattern, code)
        if not match:
            raise HTTPException(status_code=422, detail={"error": "رمز وارد شده صحیح نمی باشد"})
        return code



    @validator("MobileNumber")
    def validate_mobile_num(cls, delivery_mobile_number):
        # sourcery skip: instance-method-first-arg-name
        pattern = r"^09[0-9]{9}$"
        match = re.fullmatch(pattern, delivery_mobile_number)
        if not match:
            raise HTTPException(status_code=422, detail={"error": "شماره تلفن وارد شده صحیح نمیباشد"})
        return delivery_mobile_number

    @validator("FirstName")
    def first_name(cls, first_name):
        # sourcery skip: instance-method-first-arg-name
        pattern = r"^[\u0600-\u06FF ]{2,32}$"
        match = re.fullmatch(pattern, first_name)
        if not match:
            raise HTTPException(status_code=422, detail={"error": "نام وارد شده صحیح نمیباشد"})
        return first_name

    @validator("LastName")
    def lastname(cls, lastname):
        # sourcery skip: instance-method-first-arg-name
        pattern = r"^[\u0600-\u06FF ]{2,32}$"
        match = re.fullmatch(pattern, lastname)
        if not match:
            raise HTTPException(status_code=422, detail={"error": "نام خانوادگی وارد شده صحیح نمیباشد"})
        return lastname


