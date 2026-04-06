from pydantic import BaseModel
class UserCreate(BaseModel):
    username: str
    email: str


class UserOut(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True


class PostCreate(BaseModel):
    title: str
    content: str
    user_id: int


class PostUpdate(BaseModel):
    title: str
    content: str
    user_id: int


class PostOut(BaseModel):
    id: int
    title: str
    content: str
    user_id: int

    class Config:
        from_attributes = True