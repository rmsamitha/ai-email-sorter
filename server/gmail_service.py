"""
Gmail API service for fetching emails.
Requires OAuth 2.0 access tokens with Gmail API scope.
"""
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timezone
import os
import json
import base64
from typing import List, Dict, Optional


# Gmail API scope
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def get_gmail_service(access_token: str, refresh_token: Optional[str] = None) -> object:
    """
    Create and return Gmail API service instance.
    
    Args:
        access_token: OAuth 2.0 access token
        refresh_token: OAuth 2.0 refresh token (optional)
    
    Returns:
        Gmail API service object
    """
    credentials = Credentials(
        token=access_token,
        refresh_token=refresh_token,
        token_uri='https://oauth2.googleapis.com/token',
        client_id=os.getenv('GOOGLE_CLIENT_ID'),
        client_secret=os.getenv('GOOGLE_CLIENT_SECRET')
    )
    
    service = build('gmail', 'v1', credentials=credentials)
    return service


def fetch_emails_since_date(
    access_token: str,
    refresh_token: Optional[str],
    since_date: datetime,
    max_results: int = 100
) -> List[Dict]:
    """
    Fetch emails from Gmail account since a given date.
    
    Args:
        access_token: OAuth 2.0 access token
        refresh_token: OAuth 2.0 refresh token
        since_date: DateTime to fetch emails from (inclusive)
        max_results: Maximum number of emails to return
    
    Returns:
        List of email dictionaries with parsed information
    """
    try:
        service = get_gmail_service(access_token, refresh_token)
        
        # Convert datetime to Unix timestamp (seconds) for Gmail API
        # Gmail API uses Unix timestamp in seconds
        #timestamp_seconds = int(since_date.timestamp())
        
        # Query Gmail API for messages after the given date
        query = f'-in:archived'
        
        # Fetch message list
        results = service.users().messages().list(
            userId='me',
            q=query,
        ).execute()
        
        # print results in json format
        # print("msg list result in json format: ", json.dumps(results, indent=4))

        messages = results.get('messages', [])
        emails = []
        
        
        # Fetch full message details
        for msg in messages:
            message = service.users().messages().get(
                userId='me',
                id=msg['id'],
                format='metadata',
                metadataHeaders=['From', 'Subject', 'Date']
            ).execute()

            #print("single message in json format: ", json.dumps(message, indent=4))

            # Extract full message body
            print("Full message body: ", body_text)

            
            # Parse message headers
            headers = {h['name']: h['value'] for h in message['payload'].get('headers', [])}
            
            # Extract email information
            email_data = {
                'id': message['id'],
                'subject': headers.get('Subject', '(No Subject)'),
                'sender': headers.get('From', 'Unknown'),
                'body': message.get('snippet', ''),
                'received_at': _parse_date(headers.get('Date', ''))
            }
            
            emails.append(email_data)
        
        return emails
        
    except Exception as e:
        raise Exception(f"Error fetching emails from Gmail API: {str(e)}")


def _extract_message_body(message: Dict) -> str:
    """
    Extract the full message body text from Gmail API message object.
    
    Args:
        message: Gmail API message object with full format
    
    Returns:
        Message body text as string
    """
    try:
        payload = message.get('snippet', {})

        print(">>>>>> payload: ", payload)
        
        # Check if message has a simple body (plain text or HTML)
        if 'body' in payload and payload['body'].get('data'):
            print(">>>>>> message has a simple body")
            # Decode base64 encoded body
            body_data = payload['body']['data']
            body_text = base64.urlsafe_b64decode(body_data).decode('utf-8')
            return body_text
        
        # Check if message is multipart (has parts)
        if 'parts' in payload:
            print(">>>>>> message is multipart (has parts)")
            plain_text = None
            html_text = None
            
            for part in payload.get('parts', []):
                mime_type = part.get('mimeType', '')
                if mime_type == 'text/plain' and part.get('body', {}).get('data'):
                    body_data = part['body']['data']
                    plain_text = base64.urlsafe_b64decode(body_data).decode('utf-8')
                elif mime_type == 'text/html' and part.get('body', {}).get('data'):
                    body_data = part['body']['data']
                    html_text = base64.urlsafe_b64decode(body_data).decode('utf-8')
                # Handle nested parts (multipart/alternative)
                elif 'parts' in part:
                    for nested_part in part.get('parts', []):
                        nested_mime_type = nested_part.get('mimeType', '')
                        if nested_mime_type == 'text/plain' and nested_part.get('body', {}).get('data'):
                            body_data = nested_part['body']['data']
                            plain_text = base64.urlsafe_b64decode(body_data).decode('utf-8')
                        elif nested_mime_type == 'text/html' and nested_part.get('body', {}).get('data'):
                            body_data = nested_part['body']['data']
                            html_text = base64.urlsafe_b64decode(body_data).decode('utf-8')
            
            # Prefer plain text over HTML
            if plain_text:
                return plain_text
            elif html_text:
                return html_text
        
        return ''
    except Exception as e:
        print(f"Error extracting message body: {str(e)}")
        return ''


def _parse_date(date_str: str) -> datetime:
    """
    Parse email date string to datetime.
    Falls back to current UTC time if parsing fails.
    """
    if not date_str:
        return datetime.now(timezone.utc)
    
    try:
        # Try parsing common email date formats
        from email.utils import parsedate_to_datetime
        parsed_date = parsedate_to_datetime(date_str)
        # Ensure timezone-aware
        if parsed_date.tzinfo is None:
            return parsed_date.replace(tzinfo=timezone.utc)
        return parsed_date
    except:
        return datetime.now(timezone.utc)

