import bcrypt

# Function to hash a password
def hash_password(plain_password):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed_password

# Function to check if the plain password matches the hashed password
def check_password(plain_password, hashed_password):
    # Use bcrypt to check if the plain password matches the hashed password
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

if __name__ == '__main__':
    # Example usage
    plain_password = 'Ch@1tanya'

    # Hash the plain password (this would typically be done when storing the password)
    hashed_password = "$2a$08$rsMOWTFFyAg7Qyv6aXnAS.hevTQ9FVJPJYgZ9EevAzNe1ZQF/hyh."

    # Check if the plain password matches the hashed password
    is_correct = check_password(plain_password, hashed_password)
    print(f'Password match: {is_correct}')

    # Test with an incorrect password
    is_correct = check_password(plain_password, hashed_password)
    print(f'Password match with wrong password: {is_correct}')
