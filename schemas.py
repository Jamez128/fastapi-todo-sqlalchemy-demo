from pydantic import BaseModel, EmailStr
from typing import Optional

# ---- User Schemas ----
class UserCreate(BaseModel):
    username: str
    email: EmailStr

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True # allows conversion from SQLAlchemy model -> Pydantic

# ---- Todo Schemas ----
class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    done: bool = False

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    done: Optional[bool] = None

class TodoOut(BaseModel):
    id: int
    title: str
    description: str
    done: bool
    owner_id: int

    class Config:
        orm_mode = True