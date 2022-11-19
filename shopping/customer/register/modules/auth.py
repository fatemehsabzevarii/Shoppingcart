from datetime import timedelta

from passlib.context import CryptContext


class AuthHandler:
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

    def generate_hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, user_password: str, hashed_password: str) -> str:
        return self.pwd_context.verify(user_password, hashed_password)
