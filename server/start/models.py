from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql.mysqldb import MySQLDialect_mysqldb
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.dialects import registry


class MySQLDialect_cloudsql(MySQLDialect_mysqldb):

    @classmethod
    def get_pool_class(cls, url):
        # Cloud SQL connections die at any moment
        return NullPool

registry.register("cloudsql", "start.models", "MySQLDialect_cloudsql")

db = SQLAlchemy()
NORMAL_STRING = 255


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    wechat_id = db.Column(db.String(NORMAL_STRING), unique=True)
    first_name = db.Column(db.String(NORMAL_STRING))
    last_name = db.Column(db.String(NORMAL_STRING))
    phone = db.Column(db.String(NORMAL_STRING))


class Order(db.Model):
    id = db.Column(db.String(NORMAL_STRING), primary_key=True)
    event_id = db.Column(db.Integer(), db.ForeignKey('event.id'))
    event = db.relationship('Event')
    first_name = db.Column(db.String(NORMAL_STRING))
    last_name = db.Column(db.String(NORMAL_STRING))
    phone = db.Column(db.String(NORMAL_STRING))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    user = db.relationship('User')
    rental = db.Column(db.Integer)
    lift = db.Column(db.Integer)
    bus = db.Column(db.Integer)
    helmet = db.Column(db.Integer)
    beginner = db.Column(db.Integer)
    status = db.Column(db.Enum('PENDING', 'FAILED', 'PAID'))
    total = db.Column(db.Integer)
    paypal_token = db.Column(db.String(NORMAL_STRING))
    create_time = db.Column(db.DateTime)
    location = db.Column(db.String(NORMAL_STRING))
    rental_type = db.Column(db.String(NORMAL_STRING))


class Event(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    description = db.Column(db.String(NORMAL_STRING))
    rental = db.Column(db.Integer)
    lift = db.Column(db.Integer)
    helmet = db.Column(db.Integer)
    beginner = db.Column(db.Integer)
    bus = db.Column(db.Integer)
    ticket_num = db.Column(db.Integer)
    event_date = db.Column(db.Date)

    @hybrid_property
    def ticket_left(self):
        paid_count = Order.query.filter_by(
            event_id=self.id,
            status='PAID',
            bus=True
        ).count()
        return self.ticket_num - paid_count
