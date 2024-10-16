import hashlib
import base64
import os
import requests

# Step 1: Generate code_verifier and code_challenge
def generate_code_verifier():
    return base64.urlsafe_b64encode(os.urandom(32)).decode('utf-8').rstrip('=')

def generate_code_challenge(code_verifier):
    code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    return base64.urlsafe_b64encode(code_challenge).decode('utf-8').rstrip('=')

# Your credentials
client_id = '98219bfb3011a129dbd9f4a40f569de4'
redirect_uri = 'https://www.google.com/'
authorization_endpoint = 'https://opensource-demo.orangehrmlive.com/web/index.php/oauth2/authorize'

# Generate the code_verifier and code_challenge
code_verifier = generate_code_verifier()
code_challenge = generate_code_challenge(code_verifier)

# Step 2: Authorize the user by generating the authorization request URL
auth_url = f"{authorization_endpoint}?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&code_challenge_method=S256&code_challenge={code_challenge}"
print(f"Visit the following URL to authorize: {auth_url}")

# You will need to manually visit the generated URL, log in, and retrieve the authorization code from the redirected URL.
authorization_code = input("Enter the authorization code from the redirect URL: ")


# Step 3: Token request parameters
token_endpoint = 'https://opensource-demo.orangehrmlive.com/web/index.php/oauth2/token'

data = {
    'grant_type': 'authorization_code',
    'client_id': client_id,
    'code': authorization_code,
    'redirect_uri': redirect_uri,
    'code_verifier': code_verifier
}

# Step 4: Request the access token
response = requests.post(token_endpoint, data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})

# Parse the token response
if response.status_code == 200:
    token_data = response.json()
    access_token = token_data['access_token']
    refresh_token = token_data.get('refresh_token', None)
    print(f"Access Token: {access_token}")
    print(f"Refresh Token: {refresh_token}")
else:
    print(f"Failed to obtain access token: {response.status_code}")
    print(response.text)
