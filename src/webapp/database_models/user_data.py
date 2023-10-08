from webapp import db
from flask_login import UserMixin
import smtplib, ssl


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    credential_id = db.Column(db.Integer, db.ForeignKey('credential.id'))
    child_user = db.relationship('Credential', back_populates='user')
    full_name = db.Column(db.String(150))
    CNP = db.Column(db.String(10))
    series = db.Column(db.String(150))
    number = db.Column(db.Integer)
    personal_adress = db.Column(db.String(150))
    addresses_of_interest = db.relationship("AddressOfInterest", uselist=True, back_populates = "chil_addresses_of_interest")


class AddressOfInterest(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    chil_addresses_of_interest = db.relationship('User', back_populates='addresses_of_interest')
    address_string = db.Column(db.String(150))
    address_name = db.Column(db.String(150))


def send_email(mail_receiver):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "inscrieri@euroavia-bucuresti.ro"
    password = "EuroaviaEA21"
    message = """\
    Subject: Hi there

    This message is sent from Python."""

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, mail_receiver, message)
