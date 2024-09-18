from flask import Blueprint, request, jsonify
from datetime import datetime
from app.extensions import db
from app.models.subscription import Subscription  # Import your Subscription model

subscription = Blueprint('subscription', __name__, url_prefix='/api/v1/subscription')

@subscription.route('/create', methods=['POST'])
def create_subscription():
    data = request.get_json()

    if not data or 'email' not in data or 'frequency' not in data:
        return jsonify({'error': 'Invalid request'}), 400

    email = data['email']
    frequency = data['frequency']

    try:
        new_subscription = Subscription(email=email, frequency=frequency)
        db.session.add(new_subscription)
        db.session.commit()
        return jsonify({'message': 'Subscription created successfully', 'subscription': new_subscription.serialize()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.session.close()

@subscription.route('/<int:id>', methods=['GET'])
def get_subscription(id):
    subscription = Subscription.query.get_or_404(id)
    return jsonify({
        'id': subscription.id,
        'email': subscription.email,
        'frequency': subscription.frequency,
        'created_at': subscription.created_at.isoformat()
    })

@subscription.route('/<int:id>', methods=['PUT'])
def update_subscription(id):
    subscription = Subscription.query.get_or_404(id)
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Invalid request'}), 400

    try:
        subscription.email = data.get('email', subscription.email)
        subscription.frequency = data.get('frequency', subscription.frequency)
        subscription.updated_at = datetime.now()

        db.session.commit()
        return jsonify({'message': 'Subscription updated successfully', 'subscription': subscription.serialize()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.session.close()

@subscription.route('/<int:id>', methods=['DELETE'])
def delete_subscription(id):
    subscription = Subscription.query.get_or_404(id)

    try:
        db.session.delete(subscription)
        db.session.commit()
        return jsonify({'message': 'Subscription deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.session.close()

