"""
Background service to periodically sync user inbox emails and save metadata to database.
"""
from sqlalchemy.orm import Session
from models.db_models import UserAccount, Email
from gmail_service import fetch_emails_since_date
from datetime import datetime, timedelta, timezone
from database.database import SessionLocal
import asyncio
import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request as GoogleRequest
import logging

logger = logging.getLogger(__name__)

# Track running background tasks per user
running_tasks = {}


