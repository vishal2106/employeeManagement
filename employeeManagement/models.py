from dataclasses import dataclass
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from employeeManagement import db
from werkzeug.security import generate_password_hash, check_password_hash
from secrets import token_urlsafe


def generate_token():
    return token_urlsafe(20)


def generate_hash(token):
    return generate_password_hash(token)


def _check_token(hash, token):
    return check_password_hash(hash, token)


class Role:
    ADMIN = 1
    EMPLOYEE = 2


class Remember(db.Model):
    __tablename__ = "remembers"

    id = db.Column(db.Integer(), primary_key=True)
    remember_hash = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"), index=True, nullable=False)

    def __init__(self, user_id):
        self.token = generate_token()
        self.remember_hash = generate_hash(self.token)
        self.user_id = user_id

    def check_token(self, token):
        return _check_token(self.remember_hash, token)


@dataclass
class User(db.Model):
    id: int
    username: str
    first_name: str
    last_name: str
    phone: int
    dob: str
    email: str
    location: str

    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255))
    phone = db.Column(db.Integer())
    dob = db.Column(db.Date(), nullable=False)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    remember_hashes = db.relationship("Remember", backref="user", lazy="dynamic", cascade="all, delete-orphan")
    role_id = db.Column(db.Integer())

    def __init__(self, username="", first_name="", last_name="", phone=0, dob=datetime.now(), email="", password="",
                 location="", role_id=Role.ADMIN):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.dob = dob
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.location = location
        self.role_id = role_id

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        raise AttributeError("Password should not be read like this")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_authenticated(self):
        return not "" == self.username

    def is_anonymous(self):
        return "" == self.username

    def get_remember_token(self):
        remember_instance = Remember(self.id)
        db.session.add(remember_instance)
        return remember_instance.token

    def check_remember_token(self, token):
        if token:
            for remember_hash in self.remember_hashes:
                if remember_hash.check_token(token):
                    return True
        return False

    def forget(self):
        self.remember_hashes.delete()

    def is_admin(self):
        return self.role_id == Role.ADMIN

    def is_role(self, role):
        return self.role_id == role

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
