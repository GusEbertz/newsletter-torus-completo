from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import re

db = SQLAlchemy()

class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    subscribed_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    ip_address = db.Column(db.String(45), nullable=True)  # Para IPv4 e IPv6
    
    def __repr__(self):
        return f'<Subscriber {self.email}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'subscribed_at': self.subscribed_at.isoformat(),
            'is_active': self.is_active
        }
    
    @staticmethod
    def is_valid_email(email):
        """Validação robusta de email"""
        if not email or len(email) > 120:
            return False
        
        # Regex mais rigoroso para validação de email
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email.strip()) is not None
    
    @staticmethod
    def sanitize_email(email):
        """Sanitizar email removendo espaços e convertendo para minúsculo"""
        if not email:
            return None
        return email.strip().lower()

