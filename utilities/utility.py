from datetime import datetime, timedelta

def get_current_ist_time():
    # Get the current UTC time
    current_utc_time = datetime.utcnow()

    # Add 5 hours and 30 minutes to UTC
    ist_offset = timedelta(hours=5, minutes=30)
    ist_time = current_utc_time + ist_offset

    # Return only the date and time components
    return ist_time.date(), ist_time.time()