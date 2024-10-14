from datetime import datetime, timedelta
from flask import session

def get_current_ist_time():
    # Get the current UTC time
    current_utc_time = datetime.utcnow()

    # Add 5 hours and 30 minutes to UTC
    ist_offset = timedelta(hours=5, minutes=30)
    ist_time = current_utc_time + ist_offset

    # Return only the date and time components
    return ist_time.date(), ist_time.time()

def get_data_from_session():
    name = session.get('name')
    role = session.get('role')
    if role == '1':
        role = "Employee"
    elif role == '2':
        role = "Admin"
    elif role == '3':
        role = "Sales"
    elif role == '4':
        role = "Developer"
    else:
        role = role
    return {'name':name,'role':role}