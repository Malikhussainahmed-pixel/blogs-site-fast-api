from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import Select
from app.utils import verify
from ..database import get_db
from .. import schemas, models, utils, oauth2

router = APIRouter(
    tags=['authentication']
)


@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    query = (Select(models.Users).where(
        models.Users.email == user_credentials.username))

    user = db.scalar(query)

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={
                            "message": "Invalid Credentials"})

    verifyPassword = utils.verify(user_credentials.password, user.password)

    if not verifyPassword:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={
                            "message": "Invalid Credentials"})

    token = oauth2.create_access_token({'user_id': user.id})

    return {"access_token": token, 'token_type': "bearer"}
