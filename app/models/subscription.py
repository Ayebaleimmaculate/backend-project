from datetime import datetime
from app.extensions import db

class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    frequency = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, email, frequency):
        self.email = email
        self.frequency = frequency

    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'frequency': self.frequency,
            'created_at': self.created_at.isoformat()
        }
