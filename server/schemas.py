from pydantic import BaseModel
from typing import Optional


# Category Schemas
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    account_id: int


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True


# Google Auth Schema
class GoogleAuthRequest(BaseModel):
    client_id: str
    credential: str

