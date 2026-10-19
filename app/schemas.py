from typing import Optional, Literal

from pydantic import BaseModel, EmailStr
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

    class Config:
        from_attributes = True


class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    email: str
    created_at: datetime


class PostResponse(PostBase):
    id: int
    created_at: datetime


class PostsResponse(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserOut


class PostOut(BaseModel):
    Post: PostsResponse
    total_likes: int

    class Config:
        from_attributes = True


class Post_update(PostBase):
    pass


class Post_Update_Response(PostBase):
    pass


class UsersBase(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class Create_User(UsersBase):
    pass


class Create_User_Response(BaseModel):
    id: int
    email: str
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class Likes(BaseModel):
    post_id: int
    like_dir: Literal[0, 1]
