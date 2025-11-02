from fastapi import Depends, HTTPException, status, Cookie
from sqlalchemy.orm import Session
from database.database import get_db
from models.db_models import UserAccount
import jwt
import os
from dotenv import load_dotenv

load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")


def get_current_user(
    token: str | None = Cookie(None, alias="token"),
    db: Session = Depends(get_db)
) -> UserAccount:
    # Debug: print the token value
    print(f"Token from cookie: {token[:50] if token else 'None'}...")
    """
    Dependency function to verify JWT token from cookie and get current user.
    Use this in protected endpoints that require authentication.
    
    Example:
        @app.get("/protected")
        async def protected_route(user: UserAccount = Depends(get_current_user)):
            return {"user_id": user.id}
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated. Please log in.",
        )
    
    try:
        # Decode and verify the JWT token
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user_id: int = payload.get("userId")
        email: str = payload.get("email")
        
        if user_id is None or email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )
        
        # Get user from database
        user = db.query(UserAccount).filter(UserAccount.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )
        
        return user
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired. Please log in again.",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token. Please log in again.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication error: {str(e)}",
        )

