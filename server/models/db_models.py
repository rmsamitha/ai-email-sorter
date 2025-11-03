from sqlalchemy import (
    Column, String, Text, DateTime, ForeignKey, Integer
)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime, timezone

Base = declarative_base()


class UserAccount(Base):
    __tablename__ = "user_accounts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    gmail_address = Column(String, nullable=False, unique=True)

    name = Column(String, nullable=True)
    picture = Column(String, nullable=True)
    
    # OAuth 2.0 tokens for Gmail API access
    access_token = Column(Text, nullable=True)  # OAuth 2.0 access token
    refresh_token = Column(Text, nullable=True)  # OAuth 2.0 refresh token

    # Relationships
    categories = relationship("Category", back_populates="account", cascade="all, delete-orphan")
    emails = relationship("Email", back_populates="account", cascade="all, delete-orphan")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    account_id = Column(Integer, ForeignKey("user_accounts.id"), nullable=False)

    # Relationship
    account = relationship("UserAccount", back_populates="categories")
    emails = relationship("Email", back_populates="category", cascade="all, delete-orphan")


class Email(Base):
    __tablename__ = "emails"

    gmail_msg_id = Column(String, primary_key=True)
    account_id = Column(Integer, ForeignKey("user_accounts.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    received_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    summary = Column(Text)
    summary_created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    subject = Column(String, nullable=True)
    sender = Column(String, nullable=True)
    body = Column(Text, nullable=True)

    # Relationships
    account = relationship("UserAccount", back_populates="emails")
    category = relationship("Category", back_populates="emails")