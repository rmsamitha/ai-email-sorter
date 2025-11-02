from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
import os
from typing import Generator
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database URL from environment variable, with fallback
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost:5432/email_sorter"
)

# Create engine
engine = create_engine(
    DATABASE_URL,
    poolclass=StaticPool if "sqlite" in DATABASE_URL else None,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function to get database session.
    Use this in FastAPI route dependencies.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database tables.
    Call this to create all tables defined in models.
    """
    print(f"Initializing database tables with URL: {DATABASE_URL}")
    from models.db_models import Base
    Base.metadata.create_all(bind=engine)

    print("Database tables created successfully")
    
    # Test database connection
    try:
        db = next(get_db())
        # query table test_table to test the connection
        result = db.execute(text("SELECT * FROM test_table"))
        print(result.fetchall())
        db.close()
        print("Database connection test successful")
    except Exception as e:
        print(f"Database connection test failed: {e}")
        db.close()

