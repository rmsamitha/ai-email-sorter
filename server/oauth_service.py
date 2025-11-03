"""
OAuth 2.0 service for Gmail API access.
Handles the authorization flow and token management.
"""
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
from typing import Tuple, Optional
from dotenv import load_dotenv

load_dotenv()

# Gmail API scope
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# OAuth 2.0 redirect URI (must match Google Cloud Console configuration)
REDIRECT_URI = os.getenv(
    'OAUTH_REDIRECT_URI',
    'http://localhost:8000/oauth/callback'
)

'''
def get_oauth_flow() -> Flow:
    """
    Create and return OAuth 2.0 flow instance.
    
    Returns:
        Flow instance configured with client credentials
    """

    client_id = os.getenv('GOOGLE_CLIENT_ID')
    client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        raise ValueError(
            "GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET must be set in environment variables"
        )
    
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": client_id,
                "client_secret": client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [REDIRECT_URI]
            }
        },
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    
    return flow
'''
'''
def get_authorization_url(user_id: int) -> Tuple[str, str]:
    """
    Generate OAuth 2.0 authorization URL.
    
    Args:
        user_id: User ID to include in state parameter for security
    
    Returns:
        Tuple of (authorization_url, state)
    """
    flow = get_oauth_flow()
    
    # Include user_id in state to verify on callback
    state = str(user_id)
    
    authorization_url, _ = flow.authorization_url(
        access_type='offline',  # Request refresh token
        include_granted_scopes='false',  # Only request the specific scopes we need
        state=state,
        prompt='consent'  # Force consent screen to get refresh token
    )
    print("authorization_url: ", authorization_url)
    print("state: ", state)
    
    return authorization_url, state
'''

'''

def exchange_code_for_tokens(authorization_code: str) -> Tuple[str, Optional[str]]:
    """
    Exchange authorization code for access and refresh tokens.
    
    Args:
        authorization_code: Authorization code from OAuth callback
    
    Returns:
        Tuple of (access_token, refresh_token)
    """
    # Create a new flow for token exchange
    # We need to recreate the flow with the actual granted scopes
    # instead of strictly validating against initial SCOPES
    client_id = os.getenv('GOOGLE_CLIENT_ID')
    client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        raise ValueError(
            "GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET must be set in environment variables"
        )
    
    # Create a new flow that accepts the granted scopes from the callback
    # We need to include all potentially granted scopes to avoid validation errors
    # The user may have already granted userinfo scopes from Google Sign-In
    all_potential_scopes = [
        'https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile',
        'openid'
    ]
    
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": client_id,
                "client_secret": client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [REDIRECT_URI]
            }
        },
        scopes=all_potential_scopes,  # Accept all potential scopes that might be granted
        redirect_uri=REDIRECT_URI
    )
    
    # Exchange authorization code for tokens
    # This will accept whatever scopes were actually granted
    flow.fetch_token(code=authorization_code)
    
    credentials = flow.credentials
    
    # Verify that we got at least the Gmail readonly scope
    granted_scopes = credentials.scopes if hasattr(credentials, 'scopes') else []
    required_scope = 'https://www.googleapis.com/auth/gmail.readonly'
    
    if required_scope not in granted_scopes:
        # Check if any Gmail scope is present (more flexible)
        has_gmail_scope = any('gmail' in scope.lower() for scope in granted_scopes)
        if not has_gmail_scope:
            raise ValueError(
                f"Required Gmail scope not granted. Granted scopes: {granted_scopes}"
            )
    
    print(f"Successfully exchanged code for tokens. Granted scopes: {granted_scopes}")
    return credentials.token, credentials.refresh_token
'''

'''
def refresh_access_token(refresh_token: str) -> str:
    """
    Refresh an expired access token using refresh token.
    
    Args:
        refresh_token: OAuth 2.0 refresh token
    
    Returns:
        New access token
    """
    client_id = os.getenv('GOOGLE_CLIENT_ID')
    client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        raise ValueError(
            "GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET must be set in environment variables"
        )
    
    credentials = Credentials(
        token=None,  # No current token
        refresh_token=refresh_token,
        token_uri='https://oauth2.googleapis.com/token',
        client_id=client_id,
        client_secret=client_secret
    )
    
    # Refresh the token
    credentials.refresh(Request())
    
    return credentials.token
'''

'''

def verify_token_validity(access_token: str, refresh_token: Optional[str]) -> bool:
    """
    Verify if access token is still valid.
    If invalid and refresh_token is available, refresh it.
    
    Args:
        access_token: Current access token
        refresh_token: Refresh token (optional)
    
    Returns:
        True if token is valid or was refreshed, False otherwise
    """
    try:
        # Try to use the token to make a simple API call
        credentials = Credentials(
            token=access_token,
            refresh_token=refresh_token,
            token_uri='https://oauth2.googleapis.com/token',
            client_id=os.getenv('GOOGLE_CLIENT_ID'),
            client_secret=os.getenv('GOOGLE_CLIENT_SECRET')
        )
        
        # Try to build Gmail service to verify token
        service = build('gmail', 'v1', credentials=credentials)
        service.users().getProfile(userId='me').execute()
        
        return True
    except Exception:
        # Token is invalid
        return False

'''