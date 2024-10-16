import requests

access_token = """
def502001f64fdfdc63165f8f62269dba1e133d0727e6ef8c84b9ce32ca18ee0a9f05f7f63f3704af82ed481dcf76956ea382fabf8b66a5668e94d190071d6d1d2e1eed28ac86645eb6d4b0900efcf6e5da9e9dfd87527a2b2da77019089b3be8a2cc8a8f9ff073f8a64933cc54967ce440462c01142766f071771d19fcd37015cb6de198df5be6ed000fd6ef1408f32641769d8746d3539cd52c8b53c3ea442fafafce0
"""
# Example API request to fetch user details
api_url = 'https://opensource-demo.orangehrmlive.com/api/v2/employees'  # Adjust URL
headers = {
    'Authorization': f'Bearer {access_token}',  # Ensure the access_token is valid
    'Content-Type': 'application/json'
}

response = requests.get(api_url, headers=headers)

# Check if the response was successful
if response.status_code == 200:
    try:
        print(response.json())
    except requests.exceptions.JSONDecodeError:
        print("Error decoding JSON response")
else:
    print(f"Request failed with status code: {response.status_code}")
    print(response.text)  # Print the response content to see what the error is
    print(response.json())
