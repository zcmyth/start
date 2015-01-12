# -*- coding: utf-8 -*-

from datetime import datetime
from flask.ext.script import Manager
from start import create_app
from settings import DEV as ENV
from flask.ext.migrate import Migrate, MigrateCommand
from start.models import Event, Ticket, Order

app = create_app(ENV)
manager = Manager(app)

migrate = Migrate(app, app.db)
manager.add_command('db', MigrateCommand)

EVENT_ID = 3
EVENT_NAME = 'Ski|Snowboarding Day Trip to Hunter Mountain Jan 18'


@manager.command
def update_event():
    event = Event(
        id=EVENT_ID,
        description=EVENT_NAME,
        rental=34,
        lift=54,
        lesson=62,
        bus=42,
        ticket_num=56
    )
    app.db.session.merge(event)
    app.db.session.commit()


@manager.command
def update_ticket():
    ticket = Ticket(
        id=EVENT_ID,
        description=EVENT_NAME,
        lift=64,
        snowboard=34,
        ski=34
    )
    app.db.session.merge(ticket)
    app.db.session.commit()


@manager.command
def add_xuning():
    order = Order(
        id='XXXXXXXX',
        event_id=EVENT_ID,
        first_name='Ning',
        last_name='Xu',
        phone='',
        email='',
        bus=1,
        lift=1,
        rental=1,
        lesson=0,
        location='NEW_PORT',
        status='PAID',
        create_time=datetime.utcnow(),
        total=0,
        rental_type='SKI'
    )
    app.db.session.merge(order)
    app.db.session.commit()


if __name__ == "__main__":
    manager.run()
