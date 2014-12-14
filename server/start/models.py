from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()
NORMAL_STRING = 255


class Event(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    description = db.Column(db.String(NORMAL_STRING))
    rental = db.Column(db.Integer)
    lift = db.Column(db.Integer)
    lesson = db.Column(db.Integer)
    bus = db.Column(db.Integer)


class Order(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    event_id = db.Column(db.Integer(), db.ForeignKey('event.id'))
    event = db.relationship('Event')
    first_name = db.Column(db.String(NORMAL_STRING))
    last_name = db.Column(db.String(NORMAL_STRING))
    email = db.Column(db.String(NORMAL_STRING))
    phone = db.Column(db.String(NORMAL_STRING))
    rental = db.Column(db.Boolean)
    lift = db.Column(db.Boolean)
    lesson = db.Column(db.Boolean)
    status = db.Column(db.Enum('PENDING', 'FAILED', 'PAID'))
    total = db.Column(db.Integer)
    paypal_token = db.Column(db.String(NORMAL_STRING))
