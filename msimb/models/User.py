from msimb import db
from os import urandom
from hashlib import sha256
from base64 import b64encode
from flask.ext.login import UserMixin


def generate_salt():
    rand_bytes = urandom(256)
    return b64encode(rand_bytes).decode('utf-8')

def hash_password(password, salt):
    return sha256('{}{}'.format(salt, password).encode()).hexdigest()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False)
    salt = db.Column(db.String(), nullable=False)
    pw_hash = db.Column(db.String(), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.salt = generate_salt()
        self.pw_hash = hash_password(password, self.salt)

    def __repr__(self):
        return self.username

    def get_id(self):
        return str(self.id)

    def validate(self, password):
        return self.pw_hash == hash_password(password, self.salt)
