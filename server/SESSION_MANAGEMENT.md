# Session Management Guide

This document explains how JWT tokens and cookies are used for session management in the AI Email Sorter application.

## How It Works

### 1. **Login Flow** (`/google-auth` endpoint)

When a user logs in with Google:
1. Frontend sends Google credential to backend
2. Backend verifies Google token
3. Backend creates/finds user in database
4. Backend generates JWT token with user info
5. Backend sets HttpOnly cookie with JWT token
6. Backend returns user data in JSON response

### 2. **Cookie Storage** (Automatic)

The JWT token is stored in an **HttpOnly cookie**:
- ✅ **Automatic**: Browser stores it automatically
- ✅ **Secure**: JavaScript cannot access it (prevents XSS attacks)
- ✅ **Auto-sent**: Browser automatically includes it in all requests to the same domain
- ✅ **Expiration**: Cookie expires after 1 hour (configurable)

### 3. **Session Verification** (`/me` endpoint)

On page load or when checking authentication:
1. Frontend calls `/me` endpoint
2. Backend reads JWT token from cookie
3. Backend verifies JWT token signature
4. Backend extracts user ID from token
5. Backend fetches user from database
6. Backend returns user data if valid

### 4. **Protected Endpoints**

Any endpoint can be protected by adding `user: UserAccount = Depends(get_current_user)`:

```python
@app.get("/protected")
async def protected_route(user: UserAccount = Depends(get_current_user)):
    # This endpoint requires authentication
    # If no valid cookie, returns 401 Unauthorized
    return {"user_id": user.id}
```

### 5. **Logout Flow** (`/logout` endpoint)

When user logs out:
1. Frontend calls `/logout` endpoint
2. Backend deletes the cookie
3. Frontend clears local storage and state

## Frontend Implementation

### Making Authenticated Requests

Always include `credentials: 'include'` in fetch requests to send cookies:

```javascript
fetch(`${apiUrl}/categories`, {
  method: 'GET',
  credentials: 'include', // ← Required for cookies
})
```

### Session Verification on Page Load

The app automatically verifies session on page load:

```javascript
useEffect(() => {
  verifySession(); // Checks if user is still logged in
}, []);
```

### Handling Session Expiration

If the token expires:
1. Backend returns 401 Unauthorized
2. Frontend clears local storage
3. Frontend redirects to login page

## Security Features

### HttpOnly Cookie
- **Prevents XSS attacks**: JavaScript cannot access the token
- **Automatic**: No manual token handling needed
- **Secure**: Only sent over HTTPS in production

### JWT Token Contents
```json
{
  "userId": 1,
  "email": "user@example.com"
}
```

### Token Expiration
- Default: 1 hour (3600 seconds)
- Configurable: Change `max_age` in cookie settings
- Automatic cleanup: Cookie expires automatically

## Important Notes

1. **No Manual Token Storage**: Don't store JWT in localStorage
   - The HttpOnly cookie handles this automatically
   - More secure than localStorage

2. **Always Include Credentials**: 
   ```javascript
   credentials: 'include' // Required for cookies
   ```

3. **CORS Configuration**: 
   - Backend must allow credentials: `allow_credentials=True`
   - Frontend origin must be in `allow_origins`

4. **Production Settings**:
   - Set `secure=True` in cookie (HTTPS only)
   - Use strong `JWT_SECRET` in environment variables

## Example Usage

### Protected Endpoint (Backend)
```python
@app.post("/categories")
async def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    user: UserAccount = Depends(get_current_user)  # Requires auth
):
    # Only authenticated users can create categories
    db_category = Category(
        name=category.name,
        account_id=user.id  # Use authenticated user's ID
    )
    db.add(db_category)
    db.commit()
    return db_category
```

### Authenticated Request (Frontend)
```javascript
const createCategory = async (categoryData) => {
  const response = await fetch(`${apiUrl}/categories`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include', // Sends cookie automatically
    body: JSON.stringify(categoryData),
  });
  
  if (response.status === 401) {
    // Session expired, redirect to login
    window.location.href = '/login';
  }
  
  return response.json();
};
```

