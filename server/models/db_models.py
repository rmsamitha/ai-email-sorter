from sqlalchemy import (
    Column, String, Text, DateTime, ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime, timezone
import uuid

Base = declarative_base()


class UserAccount(Base):
    __tablename__ = "user_accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    gmail_address = Column(String, nullable=False, unique=True)
    access_token = Column(String, nullable=False)
    refresh_token = Column(String, nullable=False)

    # Relationships
    categories = relationship("Category", back_populates="account", cascade="all, delete-orphan")
    emails = relationship("Email", back_populates="account", cascade="all, delete-orphan")


class Category(Base):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(Text)
    account_id = Column(UUID(as_uuid=True), ForeignKey("user_accounts.id"), nullable=False)

    # Relationship
    account = relationship("UserAccount", back_populates="categories")
    emails = relationship("Email", back_populates="category", cascade="all, delete-orphan")


class Email(Base):
    __tablename__ = "emails"

    gmail_msg_id = Column(String, primary_key=True)
    account_id = Column(UUID(as_uuid=True), ForeignKey("user_accounts.id"), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True)
    received_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    summary = Column(Text)
    summary_created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    account = relationship("UserAccount", back_populates="emails")
    category = relationship("Category", back_populates="emails")