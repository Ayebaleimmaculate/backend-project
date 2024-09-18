from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.extensions import db  # Assuming you have SQLAlchemy instance named 'db'

class Contact(db.Model):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(20))
    message = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Contact {self.name}>"
