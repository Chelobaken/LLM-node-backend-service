from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from core.config import settings
from typing import Any
import jwt


class AuthSecurity:
    def __init__(self):
        self.ALGORITHM = "HS256"
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self, subject: str | Any, time_delta: timedelta) -> str:
        time_end = datetime.now(timezone.utc) + time_delta
        to_encode = {"time": str(time_end), "user": str(subject)}
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=self.ALGORITHM)

        return encoded_jwt

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)


authsecurity = AuthSecurity()
