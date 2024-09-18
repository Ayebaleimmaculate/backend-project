
from datetime import datetime
from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.payment import Payment

payment = Blueprint('payment',__name__, url_prefix='/api/v1/payment')

@payment.route('/process_payment', methods=['POST'])
def process_payment():
    data = request.get_json()
    amount = data.get('amount')
    currency = data.get('currency')
    description = data.get('description')

    # Validate input
    if not amount or not currency or not description:
        return jsonify({'error': 'Missing required fields.'}), 400

    try:
        # Create a new payment instance
        new_payment = Payment(amount=amount, currency=currency, description=description)
        db.session.add(new_payment)
        db.session.commit()

        # Perform actual payment processing here (integration with payment gateway, etc.)
        # For demo purposes, assume success
        new_payment.status = 'completed'
        db.session.commit()

        return jsonify({'message': 'Payment processed successfully.', 'payment_id': new_payment.id}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Route to retrieve payment details by ID
@payment.route('/payment/<int:payment_id>', methods=['GET'])
def get_payment(payment_id):
    payment = Payment.query.get(payment_id)
    if not payment:
        return jsonify({'error': 'Payment not found.'}), 404

    return jsonify({
        'id': payment.id,
        'amount': payment.amount,
        'currency': payment.currency,
        'description': payment.description,
        'status': payment.status
    }), 200

# Route to list all payments
@payment.route('/payments', methods=['GET'])
def list_payments():
    payments = Payment.query.all()
    payments_list = [{
        'id': payment.id,
        'amount': payment.amount,
        'currency': payment.currency,
        'description': payment.description,
        'status': payment.status
    } for payment in payments]

    return jsonify({'payments': payments_list}), 200

# Route to update payment status
@payment.route('/payment/<int:payment_id>', methods=['PUT'])
def update_payment(payment_id):
    data = request.get_json()
    new_status = data.get('status')

    if not new_status:
        return jsonify({'error': 'Status field is required.'}), 400

    payment = Payment.query.get(payment_id)
    if not payment:
        return jsonify({'error': 'Payment not found.'}), 404

    try:
        payment.status = new_status
        db.session.commit()

        return jsonify({'message': 'Payment status updated successfully.'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

