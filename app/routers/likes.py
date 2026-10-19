from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from .. import models, schemas, oauth2
from sqlalchemy import Select
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/likes",
    tags=["Likes"]
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def Create_vote(like: schemas.Likes, db: Session = Depends(get_db), user: models.Users = Depends(oauth2.get_current_user)):

    post = db.scalars(Select(models.Post).filter(
        models.Post.id == like.post_id)).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            "message": f"post with id {like.post_id} does not exist"})

    query = Select(models.Likes).filter(models.Likes.post_id ==
                                        like.post_id, models.Likes.user_id == user.id)

    found_like = db.scalars(query).first()

    if like.like_dir == 1:
        if found_like:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={
                                "message": f"user: {user.id} has already liked post_id:{like.post_id}"})

        addlike = models.Likes(post_id=like.post_id, user_id=user.id)
        db.add(addlike)
        db.commit()
        return {"message": "post successfuly liked"}

    else:
        if not found_like:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                                "message": f"like does not exist"})

        db.delete(found_like)
        db.commit()

        return {"message": "like from post successfuly removed"}
