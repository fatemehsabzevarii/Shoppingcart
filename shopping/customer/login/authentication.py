import time
from shopping.customer.register.models import Customer
from shopping.helper.connection import Db
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta



SECRET_KEY = "9531e151b8dde2f3c685cde1522da70d57485e33c01d748a1bf7e9bd9c352060"
JWT_EXP_DELTA_SECONDS = 20
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(phoneNumber: str,password):
    with Db():
        return Customer.objects.get(mobileNumber=phoneNumber,password=password)



def authenticate_user(phoneNumber: str, password: str):
    with Db():
        user = get_user(phoneNumber,password)


        if not user:
            return False


    return user


def create_access_token(phoneNumber):
    payload = {
        "user": phoneNumber,
        "exp":  datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS),

    }

    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token":access_token}



def decode_hash(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    except jwt.ExpiredSignatureError:
        return False
    else:
        return payload


def create_refresh_token(self):
    payload = {
        "user": self.mobileNumber,
        "exp": time.time() + 800,
    }
    refresh_token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return {"refresh_token":refresh_token}
