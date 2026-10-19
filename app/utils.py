from pwdlib import PasswordHash
from .config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
hash_password = PasswordHash.recommended()


def hash(password: str):

    return hash_password.hash(password)


def verify(user_password: str, db_hashed_password: str):

    return hash_password.verify(user_password, db_hashed_password)
