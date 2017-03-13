from app import db
from passlib.apps import custom_app_context as pwd_context


# User Model
class User(db.Model):
    __tablename__ = 'users'
    uid           = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(128), nullable=False)
    email         = db.Column(db.String(128), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __init__(self, username=None, email=None, password=None):
        self.username      = username.lower()
        self.email         = email.lower()
        self.password_hash = self.create_password_hash(password)

    def create_password_hash(self, password):
        return pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    @property
    def to_json(self):
        return {
            'uid': self.uid,
            'username': self.username,
            'email': self.email,
        }
