from . import db
from flask_login import UserMixin


class Credential(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    generated_password = db.Column(db.String(150))
    user = db.relationship('User', uselist=False, backref='credential')
