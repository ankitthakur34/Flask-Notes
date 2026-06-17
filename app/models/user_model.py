
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
    is_verified = db.Column(db.Boolean,nullable=False,default=False)

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

#  DTO - Data transfor object - when we want diffrenet represenation of a single model. 

# Where DTO Becomes Useful

# Suppose tomorrow you need:

# Admin API
# {
#   "id": 1,
#   "username": "ankit",
#   "email": "ankit@gmail.com",
#   "role": "ADMIN",
#   "created_at": "..."
# }
# Public API
# {
#   "id": 1,
#   "username": "ankit"
# }
# Profile API
# {
#   "id": 1,
#   "username": "ankit",
#   "email": "ankit@gmail.com"
# }

# Now one to_dict() cannot satisfy all three use cases.

# DTOs solve that:

# AdminUserDTO.to_response(user)

# PublicUserDTO.to_response(user)

# ProfileUserDTO.to_response(user)