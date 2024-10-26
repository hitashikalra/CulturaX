import re
from datetime import datetime

def sanitize_input(input_data):
    # Basic sanitization to prevent injection attacks
    if isinstance(input_data, str):
        return re.sub(r'[<>]', '', input_data)
    return input_data

def validate_event_data(data):
    required_fields = ['name', 'date', 'location']
    for field in required_fields:
        if field not in data or not sanitize_input(data[field]):
            return False
    try:
        datetime.strptime(data['date'], '%Y-%m-%d')
    except ValueError:
        return False
    return True

def validate_ticket_data(data):
    required_fields = ['event_id', 'user_id']
    for field in required_fields:
        if field not in data or not isinstance(data[field], int):
            return False
    return True

# Custom error handlers
def handle_bad_request(e):
    return {'error': 'Bad Request', 'message': str(e)}, 400

def handle_not_found(e):
    return {'error': 'Not Found', 'message': str(e)}, 404
