def validate_event_data(data):
    required_fields = ['name', 'date', 'location']
    for field in required_fields:
        if field not in data or not data[field]:
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
