from datetime import datetime
from app.extensions import db
from sqlalchemy import Enum

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    status = db.Column(Enum('pending', 'failed', 'completed', name='payment_status'), nullable=False, default='pending')

    def __repr__(self):
        return f'<Payment {self.id}>'
