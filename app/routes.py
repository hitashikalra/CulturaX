from flask import request, jsonify
from app import db
from app.models import Event, Ticket
from datetime import datetime
from .utils import validate_event_data, validate_ticket_data
from .errors import handle_bad_request, handle_not_found
from flask import current_app as app

@app.errorhandler(400)
def bad_request(e):
    return handle_bad_request(e)

@app.errorhandler(404)
def not_found(e):
    return handle_not_found(e)

# Route to create an event with validation
@app.route('/api/events', methods=['POST'])
def create_event():
    data = request.json
    if not validate_event_data(data):
        return jsonify({'error': 'Invalid event data'}), 400

    event = Event(
        name=data['name'], 
        date=datetime.strptime(data['date'], '%Y-%m-%d'), 
        location=data['location']
    )
    db.session.add(event)
    db.session.commit()
    return jsonify({'message': 'Event created successfully', 'event_id': event.id}), 201

# Route to list all events with optional filters
@app.route('/api/events', methods=['GET'])
def list_events():
    events = Event.query.all()
    return jsonify([
        {
            'id': event.id,
            'name': event.name, 
            'date': event.date.strftime('%Y-%m-%d'), 
            'location': event.location
        } 
        for event in events
    ])

# Route to register for an event with validation
@app.route('/api/registrations', methods=['POST'])
def register_for_event():
    data = request.json
    if not validate_ticket_data(data):
        return jsonify({'error': 'Invalid registration data'}), 400

    ticket = Ticket(
        event_id=data['event_id'], 
        user_id=data['user_id'], 
        status='registered'
    )
    db.session.add(ticket)
    db.session.commit()
    return jsonify({'message': 'Registration successful', 'ticket_id': ticket.id}), 201

# Route to view tickets for an event
@app.route('/api/events/<int:event_id>/tickets', methods=['GET'])
def list_tickets(event_id):
    tickets = Ticket.query.filter_by(event_id=event_id).all()
    return jsonify([
        {'ticket_id': ticket.id, 'user_id': ticket.user_id, 'status': ticket.status}
        for ticket in tickets
    ])

# Update an event
@app.route('/api/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    data = request.json
    if not validate_event_data(data):
        return jsonify({'error': 'Invalid data'}), 400

    event = Event.query.get(event_id)
    if not event:
        return jsonify({'error': 'Event not found'}), 404

    event.name = data['name']
    event.date = datetime.strptime(data['date'], '%Y-%m-%d')
    event.location = data['location']
    db.session.commit()

    return jsonify({'message': 'Event updated successfully'})

# Delete an event
@app.route('/api/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({'error': 'Event not found'}), 404

    db.session.delete(event)
    db.session.commit()
    return jsonify({'message': 'Event deleted successfully'})

