from . import db
from flask_login import UserMixin


class FireData(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(50))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    bright_ti_4 = db.Column(db.Float)
    scan = db.Column(db.Float)
    track = db.Column(db.Float)
    acq_date = db.Column(db.String(50))
    acq_time = db.Column(db.String(50))
    satellite = db.Column(db.String(50))
    confidence = db.Column(db.Float)
    instrument = db.Column(db.String(50))
    version = db.Column(db.String(50))
    bright_ti_5 = db.Column(db.Float)
    frp = db.Column(db.Float)
    daynight = db.Column(db.String(10))
