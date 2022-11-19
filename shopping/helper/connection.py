import os
from dotenv import load_dotenv
from mongoengine import connection



class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Db(metaclass=Singleton):
    def __init__(self):
        load_dotenv()
        self.connection = connection.register_connection(alias=os.getenv("MONGO_ALIAS"),
                                                         db=os.getenv("MONGO_DB_NAME"), name=os.getenv("MONGO_DB_NAME"),
                                                         host=os.getenv("MONGO_HOST"), username=os.getenv("MONGO_USER"),
                                                         password=os.getenv("MONGO_PASSWORD"),
                                                         authentication_source=os.getenv("MONGO_AUTH_SOURCE"))

    def __enter__(self):
        return connection.connect(alias=os.getenv("MONGO_ALIAS"),
                                  db=os.getenv("MONGO_DB_NAME"), name=os.getenv("MONGO_DB_NAME"),
                                  host=os.getenv("MONGO_HOST"), username=os.getenv("MONGO_USER"),
                                  password=os.getenv("MONGO_PASSWORD"),
                                  authentication_source=os.getenv("MONGO_AUTH_SOURCE"))

    def __exit__(self, exc_type, exc_val, exc_tb):
        connection.disconnect(os.getenv("MONGO_ALIAS"))
