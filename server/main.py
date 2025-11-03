import json
from math import log
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse, Response
from sqlalchemy.orm import Session
from typing import List
from database.database import get_db, init_db
from models.db_models import Category, UserAccount, Email
from schemas import CategoryCreate, CategoryUpdate, CategoryResponse, GoogleAuthRequest, EmailResponse, GetEmailsRequest
from gmail_service import fetch_emails_since_date
from datetime import datetime as dt
from auth import get_current_user
from google_auth_oauthlib.flow import Flow
import os
from dotenv import load_dotenv
from google.oauth2 import id_token
from google.auth.transport import requests
import jwt
from utils import summarize, categorize



load_dotenv()

init_db()

app = FastAPI(title="AI Email Sorter API", version="1.0.0")

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid",
]

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


# Email endpoints
@app.post("/emails/inbox", response_model=List[EmailResponse])
async def get_inbox_emails(
    request_body: GetEmailsRequest,
    user: UserAccount = Depends(get_current_user)
):
    """
    Get all inbox emails of the given user's Gmail account after the specified timestamp.
    
    Args:
        request_body: Contains gmail_address, timestamp, and optional max_results
        db: Database session
    
    Returns:
        List of emails from the user's Gmail inbox after the specified timestamp
    """
    try:
        # Find user by gmail_address
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with gmail_address '{request_body.gmail_address}' not found"
            )
        
        # Check if user has access token stored
        if not user.access_token:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Gmail API access not configured for user '{request_body.gmail_address}'. Please grant Gmail API access permissions."
            )
        
        # Verify and refresh token if needed
        access_token = user.access_token
        refresh_token = user.refresh_token
        
        # Try to fetch emails using the stored access token
        try:
            # Use the timestamp from request body
            since_date = request_body.timestamp
            max_results = request_body.max_results or 100
            
            # Fetch emails from Gmail API
            emails = fetch_emails_since_date(
                access_token=access_token,
                refresh_token=refresh_token,
                since_date=since_date,
                max_results=max_results
            )
            
            return emails
            
        except Exception as e:
            # If API call fails, token might be expired - try to refresh
            log.error(f"Error fetching emails: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error fetching emails: {str(e)}"
            )
                
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing request: {str(e)}"
        )


@app.post("/emails/process")
async def process_emails(
    request_body: GetEmailsRequest,
    db: Session = Depends(get_db),
    user: UserAccount = Depends(get_current_user)
):
    """
    Get all inbox emails of the given user's Gmail account after the specified timestamp.
    
    Args:
        request_body: Contains gmail_address, timestamp, and optional max_results
        db: Database session
    
    Returns:
        List of emails from the user's Gmail inbox after the specified timestamp
    """
    try:
        # Find user by gmail_address
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with gmail_address '{request_body.gmail_address}' not found"
            )
        
        # Check if user has access token stored
        if not user.access_token:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Gmail API access not configured for user '{request_body.gmail_address}'. Please grant Gmail API access permissions."
            )
        
        # Verify and refresh token if needed
        access_token = user.access_token
        refresh_token = user.refresh_token
        
        # Try to fetch emails using the stored access token
        try:
            # Use the timestamp from request body
            since_date = request_body.timestamp
            max_results = request_body.max_results or 100
            
            # Fetch emails from Gmail API
            emails = fetch_emails_since_date(
                access_token=access_token,
                refresh_token=refresh_token,
                since_date=since_date,
                max_results=max_results
            )

            
            # store email information in DB
            for email in emails:
                print(">>>>>>>>> emails: ", email)

                summary = await generateSummary(email.body)
                category = await defineCategory(user.id, email.body)
                db_email = Email(
                    gmail_msg_id=email['id'],
                    account_id=user.id,
                    category_id=category,
                    received_at=email['received_at'],
                    subject=email['subject'],
                    sender=email['sender'],
                    body=email['body'],
                    summary=summary
                )
                db.add(db_email)
                db.commit()
                db.refresh(db_email)

            return emails
            
        except Exception as e:
            # If API call fails, token might be expired - try to refresh
            print(f"Error fetching emails: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error fetching emails: {str(e)}"
            )
                
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing request: {str(e)}"
        )

async def generateSummary(email: str) -> str:
    """
    Generate a summary of the email body using OpenAI API.
    """
    contentToSummarize = {
        "subject": email['subject'],
        "body": email['body']
    }
    summary = await summarize(contentToSummarize)
    print("summary generated: ", summary)
    return summary

async def defineCategory(userId: int, email: json) -> str:
    contentToDefineCategory = {
        "subject": email['subject'],
        "body": email['body'],
        "sender": email['sender']
    }
    category = await categorize(userId, contentToDefineCategory)
    print("category generated: ", category)
    return category

@app.get("/auth/google/connect")
async def connect_google(
    db: Session = Depends(get_db),
    user: UserAccount = Depends(get_current_user)
):
    """
    Get Google OAuth authorization URL for Gmail API access.
    Returns JSON with authorization_url for frontend to redirect user.
    """
    # Gmail API scopes
    #SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    print("user id in connect_google: ", user.id)
    print("user gmail address in connect_google: ", user.gmail_address)

    try:
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                    "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/oauth/callback")],
                }
            },
            scopes=SCOPES,
            redirect_uri=os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/oauth/callback")
        )
        print(">>>> scopes in auth/google/connect: ", SCOPES)

        # Generate Google authorization URL
        # Include user_id in state for security
        state = str(user.id)
        auth_url, _ = flow.authorization_url(
            access_type="offline",
            include_granted_scopes="false",  # Only request the specific scopes we need
            state=state,
            prompt="consent"
        )

        print("authorization_url generated: ", auth_url)

        # Return JSON response with authorization URL
        # Frontend will handle the redirect using window.location.href
        return JSONResponse(
            content={
                "authorization_url": auth_url,
                "message": "Please visit the authorization URL to grant Gmail API access",
                "requires_oauth": True
            },
            status_code=200
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating authorization URL: {str(e)}"
        )


@app.get("/oauth/callback")
async def google_callback(
    request: Request,
    code: str,
    state: str,
    db: Session = Depends(get_db)
):
    print("google_callback() endpoint is running in python server")
    """Handle Google's redirect and exchange auth code for tokens"""
    
    # Gmail API scopes
    # SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    
    # Get redirect_uri - must match exactly what was used in authorization URL
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/oauth/callback")
    
    # Validate state (contains user_id)
    try:
        user_id = int(state)
        user = db.query(UserAccount).filter(UserAccount.id == user_id).first()
        
        print("User ID in oauth/callback url is found in DB as well. user.id: ", user.id, "user.gmail_address: ", user.gmail_address)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid state parameter"
        )
    
    try:
        # Create flow with the same redirect_uri used in authorization
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                    "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [redirect_uri],
                }
            },
            scopes=SCOPES,
            redirect_uri=redirect_uri  # Important: Must match authorization URL
        )
        
        print(">>>> redirect_uri: ", redirect_uri)
        print(">>>> code: ", code)
        print(">>>> state: ", state)
        print("scopes in oauth/callback: ", SCOPES)
        
        # Exchange authorization code for tokens
        # Don't pass redirect_uri - it's already set in the Flow configuration
        flow.fetch_token(code=code)
        
        print(">>>> flow.credentials: ", flow.credentials)
        
        credentials = flow.credentials
        print("tokens generated successfully. access_token: ", credentials.token, "refresh_token: ", credentials.refresh_token)
        #json stringify the credentials


    except Exception as e:
        print(f">>>> Error in google_callback: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing OAuth callback: {str(e)}"
        )

    # check in DB whether the userID already exists in the DB and then update the access_token and refresh_token
    user = db.query(UserAccount).filter(UserAccount.id == user_id).first()
    if user:
        user.access_token = credentials.token
        user.refresh_token = credentials.refresh_token
        db.commit()
        db.refresh(user)
        print("Access token and refresh token updated successfully for user: ", user.id, "gmail: ", user.gmail_address)
    else:
        # User not found - need to fetch user info from Google and create new user
        print("User not found in DB. user_id: ", user_id)
        
        # Fetch user information from Google using the access token
        try:
            # Call Google's userinfo API to get user details
            headers = {'Authorization': f'Bearer {credentials.token}'}
            userinfo_response = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', headers=headers)
            
            if userinfo_response.status_code == 200:
                userinfo = userinfo_response.json()
                gmail_address = userinfo.get('email')
                name = userinfo.get('name')
                picture = userinfo.get('picture')
                
                print(f"Fetched user info from Google: email={gmail_address}, name={name}")
                
                # Create new user with fetched information
                user = UserAccount(
                    gmail_address=gmail_address,
                    name=name,
                    picture=picture,
                    access_token=credentials.token,
                    refresh_token=credentials.refresh_token
                )
                db.add(user)
                db.commit()
                db.refresh(user)
                print(f"User added to DB successfully. user.id: {user.id}, gmail: {user.gmail_address}")
            else:
                # If userinfo API fails, raise an error
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to fetch user info from Google: {userinfo_response.status_code}"
                )
        except HTTPException:
            raise
        except Exception as e:
            print(f"Error fetching user info from Google: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating user: {str(e)}"
            )
    
    print("Redirecting to frontend (success page) with OAuth success parameter")
    

    # Redirect to frontend (success page) with OAuth success parameter
    frontend_url = os.getenv('CLIENT_HOME_URL', 'http://localhost:5173')
    return RedirectResponse(f"{frontend_url}?oauth_success=true")



@app.post("/categories", status_code=status.HTTP_201_CREATED)
async def create_category(
    category: CategoryCreate, 
    db: Session = Depends(get_db), 
    user: UserAccount = Depends(get_current_user)):
    """
    Create a new category.
    """
    print(">>>>>>>>> user id: ", user.id)

    db_category = Category(
        name=category.name,
        description=category.description,
        account_id=user.id
    )
    
    print(">>>>>>>>> user id: ", user.id)
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

