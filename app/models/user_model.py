
from app.extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(20), nullable=False, default="USER")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    notes = db.relationship('Note', backref='user', lazy=True,cascade="all, delete")

    def to_dict(self):
        return {    
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role
        }