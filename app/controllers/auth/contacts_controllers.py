from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.contacts import Contact
from http import HTTPStatus
from flask_cors import cross_origin

contacts = Blueprint('contacts', __name__, url_prefix='/api/v1/contacts')

@contacts.route('/submit', methods=['POST'])
@cross_origin()  # Allow CORS for this endpoint
def submit_contact_form():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    message = data.get('message')

    if not name or not email or not message:
        return jsonify({'error': 'Name, email, and message are required.'}), HTTPStatus.BAD_REQUEST

    new_contact = Contact(name=name, email=email, phone=phone, message=message)
    db.session.add(new_contact)
    db.session.commit()

    return jsonify({'message': 'Contact form submitted successfully!'}), HTTPStatus.CREATED

@contacts.route('/list', methods=['GET'])
@cross_origin()  # Allow CORS for this endpoint
def list_contacts():
    contacts = Contact.query.all()
    contact_list = [{
        'id': contact.id,
        'name': contact.name,
        'email': contact.email,
        'phone': contact.phone,
        'message': contact.message,
        'created_at': contact.created_at
    } for contact in contacts]

    return jsonify({'contacts': contact_list}), HTTPStatus.OK
