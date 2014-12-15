from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property

db = SQLAlchemy()
NORMAL_STRING = 255


class Order(db.Model):
    id = db.Column(db.String(NORMAL_STRING), primary_key=True)
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
    create_time = db.Column(db.DateTime)
    location = db.Column(db.String(NORMAL_STRING))


class Event(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    description = db.Column(db.String(NORMAL_STRING))
    rental = db.Column(db.Integer)
    lift = db.Column(db.Integer)
    lesson = db.Column(db.Integer)
    bus = db.Column(db.Integer)
    ticket_num = db.Column(db.Integer)

    @hybrid_property
    def ticket_left(self):
        paid_count = Order.query.filter_by(
            event_id=self.id,
            status='PAID'
        ).count()
        return self.ticket_num - paid_count
