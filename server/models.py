from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin

from config import db, bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    _password_hash = db.Column(db.String(128))

    recipes = db.relationship('Recipe', backref='user', lazy=True)

    @hybrid_property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise ValueError("Username must not be empty")
        return username

class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'
    
    pass