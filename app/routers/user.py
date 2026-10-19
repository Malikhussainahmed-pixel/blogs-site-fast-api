from .. import models, schemas, utils
from sqlalchemy import Select
from sqlalchemy.orm import Session
from ..database import get_db
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Create_User_Response)
def create_User(user: schemas.Create_User, db: Session = Depends(get_db)):

    password_hash = utils.hash(user.password)
    user.password = password_hash

    users = models.Users(**user.model_dump())

    db.add(users)
    db.commit()
    db.refresh(users)

    return users


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def get_Users(id: int, db: Session = Depends(get_db)):

    query = (Select(models.Users).where(models.Users.id == id))

    user_data = db.scalar(query)

    if user_data == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            "message": f"user with id {id} does not exit"})

    return user_data
