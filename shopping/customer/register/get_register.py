from Crypto import Hash

from shopping.customer.register.models import schemas
from shopping.customer.register.models import model_register

from shopping.customer.register.modules import hash_password
from shopping.customer.register.models.model_register import Customer



def create_user (user: UserCreate):
    hashed_password = Hash.bcrypt(Customer.password)
    db_user = Customer(phonenumber=Customer.phonenumber, hashed_password=hashed_password, is_active=False, is_admin=False)
    db_user.save()
    return db_user



def get_user(user_id: int):
    return Customer.filter(Customer.id == user_id).first()


def get_user_by_email(phonenumber: str):
    return Customer.filter(Customer.phonenumber == phonenumber).first()


def get_users(skip: int = 0, limit: int = 100):
    return list(Customer.select().offset(skip).limit(limit))


