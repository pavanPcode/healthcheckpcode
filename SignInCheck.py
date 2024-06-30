import requests
import bcrypt

def hash_password(plain_password):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed_password

# Function to check if the plain password matches the hashed password
def check_password(plain_password, hashed_password):
    # Use bcrypt to check if the plain password matches the hashed password
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def verify(mail,plain_password):
    try:
        # Define the API endpoint URL
        url = f'https://mycrm.ibizaccounts.com/api/staffs/search/{mail}'

        # Define headers (if needed)
        headers = {
            'authtoken': """eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYXBwc0BwZXJlbm5pYWxjb2RlLmluIiwibmFtZSI6IkRldmVsb3BlciIsIkFQSV9USU1FIjoxNzA4NjkzMzIwfQ.PoXlVNphTxBluptxrYSko6ENBnyO6Vgw87anIGxv0Y4""",  # Example of Authorization header
            'Content-Type': 'application/json'  # Example of Content-Type header
        }
        # Make GET request with headers
        response = requests.get(url, headers=headers)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            result = response.json()
            for i in result:
                usermailid = i['email']
                hashed_password = i['password']
                name = i['firstname']
                admin = i['admin']
                role = i['role']

                if mail == usermailid :
                    # Check if the plain password matches the hashed password
                    is_correct = check_password(plain_password, hashed_password)
                    if is_correct == True:
                        return {'status':True,'message':'Password match','name':name,'admin':admin,'role':role}
                    else:
                        return {'status': False, 'message': 'Password not match'}
                else:
                    return {'status': False, 'message': 'mailid not found'}
        else:
            # print(f"Error: {response.status_code} - {response.text}")
            return {'status': False, 'message': f"Error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {'status': False, 'message': str(e)}
