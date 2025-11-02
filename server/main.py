from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
from database.database import get_db, init_db
from models.db_models import Category, UserAccount
from schemas import CategoryCreate, CategoryUpdate, CategoryResponse, GoogleAuthRequest
from auth import get_current_user
import os
from dotenv import load_dotenv
from google.oauth2 import id_token
from google.auth.transport import requests
import jwt


load_dotenv()

init_db()

app = FastAPI(title="AI Email Sorter API", version="1.0.0")

# Configure CORS
# Get allowed origins from environment variable or use defaults
allowed_origins = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,http://localhost:3000"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/google-auth")
async def google_auth(body: GoogleAuthRequest, db: Session = Depends(get_db)):
    """
    1️⃣ Verify Google credential
    2️⃣ Find or create user
    3️⃣ Generate JWT
    4️⃣ Set cookie + return user
    """
    print("Google Auth Request came. body: ", body)
    try:
        credential = body.credential
        client_id = body.client_id

        if not credential or not client_id:
            raise HTTPException(status_code=400, detail="Missing credential or client_id")

        # 1️⃣ Verify Google token
        idinfo = id_token.verify_oauth2_token(
            credential,
            requests.Request(),
            client_id,
        )

        print("idinfo: " + str(idinfo))

        if idinfo['aud'] not in [client_id]:
           raise ValueError('Could not verify audience.')



        email = idinfo.get("email")
        name = idinfo.get("name")
        picture = idinfo.get("picture")

        # 2️⃣ Find or create user
        user = db.query(UserAccount).filter(UserAccount.gmail_address == email).first()
        if not user:
            user = UserAccount(gmail_address=email, name=name, picture=picture)
            db.add(user)
            db.commit()
            db.refresh(user)
       

        # 3️⃣ Generate JWT
        JWT_SECRET = os.getenv("JWT_SECRET", None)
        if not JWT_SECRET:
            raise HTTPException(
                status_code=500,
                detail="JWT_SECRET not configured. Please set JWT_SECRET in environment variables."
            )
        
        token_data = {"userId": user.id, "email": user.gmail_address}
        token = jwt.encode(token_data, JWT_SECRET, algorithm="HS256")

        # 4️⃣ Set cookie and return response
        response_obj = JSONResponse(
            content={
                "message": "Authentication successful", 
                "user": {
                    "id": user.id, 
                    "email": user.gmail_address, 
                    "name": user.name, 
                    "picture": user.picture
                }
            },
            status_code=200,
        )
        # Determine if we're in production (HTTPS) or development (HTTP)
        is_production = os.getenv("ENVIRONMENT", "development") == "production"

        print(f"Environment: {'production' if is_production else 'development'}")
        
        # Cookie settings:
        # - For localhost development (different ports = cross-origin):
        #   Use SameSite=None with Secure=False (Chrome allows this for localhost only)
        # - For production (HTTPS):
        #   Use SameSite=None with Secure=True (required for cross-origin)
        
        if is_production:
            # Production: HTTPS required
            response_obj.set_cookie(
                key="token",
                value=token,
                httponly=True,
                secure=True,  # HTTPS only
                max_age=3600,  # 1 hour
                samesite="none",  # Cross-origin requires "none"
                path="/",
            )
        else:
            # Development: localhost with different ports (cross-origin)
            # Chrome allows SameSite=None with Secure=False for localhost only
            response_obj.set_cookie(
                key="token",
                value=token,
                httponly=True,  # Cookie not accessible via JavaScript
                secure=True,  # Cookie sent only over HTTPS (Chrome allows False for localhost)
                max_age=3600,  # 1 hour
                samesite="none",  # Required for cross-origin (must be lowercase)
                path="/",
            )
        
        # Debug: verify cookie is being set
        print(f"Cookie 'token' set with value (first 20 chars): {token[:20]}...")
        print(f"Response headers before return: {dict(response_obj.headers)}")
        
        # Explicitly check if Set-Cookie header is present
        set_cookie_header = response_obj.headers.get('set-cookie')
        print(f"Set-Cookie header in response: {set_cookie_header}")
        
        # Verify token value is valid (not None or empty)
        if not token or len(token) < 10:
            print("ERROR: Token is invalid or too short!")
            raise HTTPException(status_code=500, detail="Failed to generate authentication token")

        return response_obj
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid Google token: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
   

@app.get("/")
async def root():
    return {"message": "Welcome to AI Email Sorter API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# Example protected endpoint - verify session
@app.get("/me")
async def get_current_user_info(user: UserAccount = Depends(get_current_user)):
    """
    Get current authenticated user info.
    Protected endpoint - requires valid JWT token in cookie.
    """
    return {
        "id": user.id,
        "email": user.gmail_address,
        "name": user.name,
        "picture": user.picture
    }


# Logout endpoint - clear cookie
@app.post("/logout")
async def logout():
    """
    Logout endpoint - clears the authentication cookie.
    Must match the same cookie settings used when setting the cookie.
    """
    is_production = os.getenv("ENVIRONMENT", "development") == "production"
    
    response = JSONResponse(
        content={"message": "Logged out successfully"},
        status_code=200,
    )
    
    # Delete cookie with same settings as when it was set
    # Must match: path, samesite, secure, and domain (if set)
    if is_production:
        response.delete_cookie(
            key="token",
            path="/",
            samesite="none",  # Must match the setting used when setting cookie (lowercase)
            secure=True,  # Must match the setting used when setting cookie
            # httponly is not needed for delete_cookie
        )
    else:
        response.delete_cookie(
            key="token",
            path="/",
            samesite="none",  # Must match the setting used when setting cookie (lowercase)
            secure=True,  # Must match the setting used when setting cookie
            # httponly is not needed for delete_cookie
        )
    
    print("Cookie 'token' deleted successfully")
    return response


@app.get("/protected")
async def protected_route(user: UserAccount = Depends(get_current_user)):
    # Only authenticated users can access
    return {"user_id": user.id}
    
# Categories CRUD Endpoints

@app.get("/categories", response_model=List[CategoryResponse])
async def get_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user: UserAccount = Depends(get_current_user)
):
    """
    Get categories for the authenticated user.
    Protected endpoint - requires valid JWT token in cookie.
    """
    # Debug: log that user is authenticated
    print(f"Categories requested for user: {user.id} ({user.gmail_address})")
    
    # Only return categories belonging to the authenticated user
    query = db.query(Category).filter(Category.account_id == user.id)
    
    categories = query.offset(skip).limit(limit).all()
    print(f"Found {len(categories)} categories for user {user.id}")
    return categories


@app.get("/categories/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: int, db: Session = Depends(get_db)):
    """
    Get a single category by ID.
    """
    category = db.query(Category).filter(Category.id == category_id).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {category_id} not found"
        )
    
    return category


@app.post("/categories", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """
    Create a new category.
    """
    db_category = Category(
        name=category.name,
        description=category.description,
        account_id=category.account_id
    )
    
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    
    return db_category


@app.put("/categories/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    category_update: CategoryUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a category (full update - all fields required except optional ones).
    """
    db_category = db.query(Category).filter(Category.id == category_id).first()
    
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {category_id} not found"
        )
    
    # Update fields
    if category_update.name is not None:
        db_category.name = category_update.name
    if category_update.description is not None:
        db_category.description = category_update.description
    
    db.commit()
    db.refresh(db_category)
    
    return db_category


@app.patch("/categories/{category_id}", response_model=CategoryResponse)
async def partial_update_category(
    category_id: int,
    category_update: CategoryUpdate,
    db: Session = Depends(get_db)
):
    """
    Partially update a category (only provided fields are updated).
    """
    db_category = db.query(Category).filter(Category.id == category_id).first()
    
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {category_id} not found"
        )
    
    # Update only provided fields
    update_data = category_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_category, field, value)
    
    db.commit()
    db.refresh(db_category)
    
    return db_category


@app.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    """
    Delete a category.
    """
    db_category = db.query(Category).filter(Category.id == category_id).first()
    
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {category_id} not found"
        )
    
    db.delete(db_category)
    db.commit()
    
    return None

