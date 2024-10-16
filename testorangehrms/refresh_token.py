import requests

# Replace these with your actual values
refresh_token = """def502002db64b61b9409a9648dca6788b2a5376a57056bd0691e91d14d538fdf59064a74a156c4c90bd38f8cd913148db765a21058fb2c29445880f2faa3478d14d1dce629136e6f9d7265397fc509c28de10f78494d58c196b20893800859d13d23ba9c86b9b6f7dab204154f248bcf7bcf623701ff942be8847f455432ec2a2a9499209ef9d7ec07153bfcc29557394ccb15594c412add8cc74e11652ac9d97c4d462ab90c32737395e701535dee98b4d3a74593c458fcd91bf29aed91a981530293676ac6a53b7572e2dada499e149a054295482f8aa2ef2f28a8753a5150fab5d3b47557f892673ecf909310a175e7a6c303ff068eb1ecf84e9e4af843df2875917d055bea6bcf8b715c6634c31b9c82a7e02cd0921089110f8ad9a45d2161e8cea5ffe960bcdb16779b6081ecda6aeaa056bf988502074e09f1b7de0d9a6c07530c55cc2f7db2b4300e9a0a21f59a0d1c7039569ffbaa597a32e18c4"""
client_id = '98219bfb3011a129dbd9f4a40f569de4'
# client_secret = "your_client_secret"  # If required by the OAuth server
redirect_uri = 'https://www.google.com/'
token_url = "https://opensource-demo.orangehrmlive.com/web/index.php/oauth2/token"

# Prepare the data for the request
data = {
    'grant_type': 'refresh_token',
    'refresh_token': refresh_token,
    'client_id': client_id,
    'redirect_uri': redirect_uri
}

# If client_secret is required, add it to the data
# data['client_secret'] = client_secret

# Send the request
response = requests.post(token_url, data=data)

# Check the response
if response.status_code == 200:
    # Parse the JSON response to get the new tokens
    token_data = response.json()
    new_access_token = token_data.get('access_token')
    new_refresh_token = token_data.get('refresh_token')  # Optional, in case the refresh token was rotated
    print("New access token:", new_access_token)
    print("New refresh token (if provided):", new_refresh_token)
else:
    # Handle error
    print(f"Error refreshing token: {response.status_code}")
    print(response.text)
