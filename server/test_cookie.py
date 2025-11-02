"""
Quick test to verify cookie is being set and sent correctly.
Check browser DevTools:
1. Network tab -> /google-auth response -> Headers -> Response Headers -> Set-Cookie
2. Network tab -> /categories request -> Headers -> Request Headers -> Cookie

The Cookie header should contain: token=<jwt_token>
"""

print("""
To verify cookie is working:

1. Check /google-auth response:
   - Open browser DevTools -> Network tab
   - Call /google-auth endpoint
   - Check Response Headers -> Should have: Set-Cookie: token=...
   
2. Check /categories request:
   - Call /categories endpoint after login
   - Check Request Headers -> Should have: Cookie: token=...
   
3. Check server logs:
   - Should print: "Cookie 'token' set with value length: ..."
   - Should print: "Token from cookie: ..." when /categories is called
""")

