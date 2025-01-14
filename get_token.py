import streamlit as st
import msal
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure OAuth2
client_id = os.getenv('AppClientId')
tenant_id = os.getenv('TenantId')
authority = f"https://login.microsoftonline.com/{tenant_id}"
scopes = ["User.Read"]
redirect_uri = "http://localhost"

# Initialize MSAL client
app = msal.PublicClientApplication(client_id, authority=authority)

# Step 2: Prompt user to paste redirect URL after login
redirect_response = st.text_input("Paste the full redirect URL after logging in:")

# Add an authentication button in Streamlit
if st.button("Login"):
    # Step 1: Generate Authorization URL
    auth_url = app.get_authorization_request_url(scopes=scopes, redirect_uri=redirect_uri)
    st.write(f"[Login here]({auth_url})")

    
  
if st.button("check"):
    # Step 3: Parse Authorization Code from Redirect Response
    from urllib.parse import urlparse, parse_qs
    query_params = parse_qs(urlparse(redirect_response).query)
    code = query_params.get("code", [None])[0]

    if code:
        # Step 4: Exchange Code for Access Token
        result = app.acquire_token_by_authorization_code(code, scopes=scopes, redirect_uri=redirect_uri)
        if "access_token" in result:
            st.success("Token acquisition successful!")
            st.write("Access Token:", result["access_token"])
            print("Access Token:", result["access_token"])
        else:
            st.error("Failed to acquire token.")
            st.error(result.get("error_description", "No further details"))
            print("Failed to acquire token:", result.get("error_description", "No further details"))
