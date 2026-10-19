import jwt
from jwt.exceptions import PyJWTError
from datetime import datetime, timedelta, timezone
from . import schemas, database, models
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import Select
from .config import settings


oauth_schema = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):

    to_encode = data.copy()

    expire_time = datetime.now(timezone.utc) + \
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({'exp': expire_time})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        id: str = payload.get('user_id')

        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=id)

    except PyJWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth_schema), db: Session = Depends(database.get_db)):

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={
                                          "message": 'could not validate credentials'}, headers={'WWW-Authenticate': 'Bearer'})

    token = verify_access_token(token, credentials_exception)

    query = Select(models.Users).where(models.Users.id == token.id)

    user = db.scalar(query)

    return user
