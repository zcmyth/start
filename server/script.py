# -*- coding: utf-8 -*-

from datetime import datetime, date
from flask.ext.script import Manager
from start import create_app
from settings import PROD as ENV
from flask.ext.migrate import Migrate, MigrateCommand
from start.models import Event, Order

app = create_app(ENV)
manager = Manager(app)

migrate = Migrate(app, app.db)
manager.add_command('db', MigrateCommand)


EVENT_ID = 8
EVENT_DATE = date(2015, 3, 14)
EVENT_NAME = 'Ski|Snowboarding Day Trip to Hunter MT ' + EVENT_DATE.strftime('%m/%d')


@manager.command
def update_event():
    event = Event(
        id=EVENT_ID,
        description=EVENT_NAME,
        event_date=EVENT_DATE,
        bus=37,
        lift=51,
        rental=34,
        beginner=68,
        helmet=9999,
        ticket_num=50
    )
    app.db.session.merge(event)
    app.db.session.commit()


@manager.command
def close_event():
    event = Event.query.get(EVENT_ID)
    event.status = 'INACTIVE'
    app.db.session.commit()


@manager.command
def add_xuning():
    order = Order(
        id='XXXXXXXX' + str(EVENT_ID),
        event_id=EVENT_ID,
        first_name='Ning',
        last_name='Xu',
        phone='',
        bus=1,
        lift=0,
        rental=0,
        helmet=0,
        beginner=0,
        location='NEW_PORT',
        status='PAID',
        create_time=datetime.utcnow(),
        total=0,
        rental_type=''
    )
    app.db.session.merge(order)
    app.db.session.commit()


if __name__ == "__main__":
    manager.run()
