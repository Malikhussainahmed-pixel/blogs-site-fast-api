from app.oauth2 import get_current_user
from app.models import Post
from .. import models, schemas, oauth2
from sqlalchemy import Select, Update, func
from sqlalchemy.orm import Session
from typing import Optional, List
from ..database import get_db
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get('/', response_model=List[schemas.PostOut])
def get_post(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    # query = Select(models.Post).filter(models.Post.title.icontains(
    #     search)).limit(limit=limit).offset(offset=skip)
    # posts = db.scalars(query).all()

    query = Select(models.Post, func.count(models.Likes.post_id).label("total_likes")).filter(models.Post.title.icontains(search)).outerjoin(
        models.Likes, models.Post.id == models.Likes.post_id).group_by(models.Post.id).order_by(models.Post.id).limit(limit=limit).offset(offset=skip)

    posts = db.execute(query).all()
    # Cursor.execute("SELECT * FROM posts")
    # posts = Cursor.fetchall()
    # print(posts)
    return posts


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_Post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.Users = Depends(oauth2.get_current_user)):
    # Cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING *""",
    #                (post.title, post.content, post.published))

    # new_post = Cursor.fetchone()
    # conn.commit()

    new_post = models.Post(user_id=current_user.id,
                           **post.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post
    # return {"Post Created": f"title:{post.title}, Content: {post.content}, published: {post.published}, rating: {post.rating}"}


@router.get('/{id}', response_model=schemas.PostOut)
def get_posts(id: int, db: Session = Depends(get_db), current_user: models.Users = Depends(oauth2.get_current_user)):

    # Cursor.execute(""" SELECT * from posts WHERE id= %s """, (str(id)))
    # post = Cursor.fetchone()

    query = Select(models.Post, func.count(models.Likes.post_id).label("total_likes")).outerjoin(
        models.Likes, models.Post.id == models.Likes.post_id).group_by(models.Post.id).filter(models.Post.id == id).order_by(models.Post.id)

    post = db.execute(query).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post not found with id: {id}")

    return post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db), current_user: models.Users = Depends(oauth2.get_current_user)):

    # Cursor.execute(
    #     """ DELETE FROM posts WHERE id= %s RETURNING *""", (str(id)))

    # deleted_post = Cursor.fetchone()

    # conn.commit()

    query = (Select(models.Post).where(models.Post.id == id))
    post = db.scalar(query)

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            "message": f"Post with id {id} does not exist"})

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={
                            "message": f"Not authorized to perform requested action"})

    db.delete(post)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    # return {"data": post_dict, "message": f"Post with id: {id} deleted"}


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post_Update_Response)
def update_post(id: int, updated_post: schemas.Post_update, db: Session = Depends(get_db), current_user: models.Users = Depends(oauth2.get_current_user)):

    # Cursor.execute(""" UPDATE posts SET title=%s , content=%s, published=%s WHERE id=%s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)))

    # updated_post = Cursor.fetchone()

    # conn.commit()

    query = Select(models.Post).where(models.Post.id == id)
    post = db.scalar(query)

    if post is None:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            "message": f"Post with id: {id} does not exist"})

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={
                            "message": f"Not authorized to perform requested action"})

    for key, value in updated_post.model_dump(exclude_unset=True).items():
        setattr(post, key, value)

    db.commit()
    db.refresh(post)
    return post
