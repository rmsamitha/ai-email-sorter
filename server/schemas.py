from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# Category Schemas
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    account_id: Optional[int] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class CategoryResponse(CategoryBase):
    id: int
    name: str
    description: Optional[str] = None
    account_id: int

# Google Auth Schema
class GoogleAuthRequest(BaseModel):
    client_id: str
    credential: str


# Email Schemas
class EmailResponse(BaseModel):
    id: str
    subject: str
    sender: str
    body: str
    received_at: datetime

    class Config:
        from_attributes = True


# OAuth Schemas
class OAuthInitiateResponse(BaseModel):
    authorization_url: str
    message: str


# Email Request Schemas
class GetEmailsRequest(BaseModel):
    gmail_address: str
    timestamp: datetime  # ISO format datetime string
    max_results: Optional[int] = 100  # Optional, defaults to 100

