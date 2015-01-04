# -*- coding: utf-8 -*-

from flask.ext.script import Manager
from start import create_app
from settings import DEV as ENV
from flask.ext.migrate import Migrate, MigrateCommand
from start.models import Event, Ticket

app = create_app(ENV)
manager = Manager(app)

migrate = Migrate(app, app.db)
manager.add_command('db', MigrateCommand)


@manager.command
def update_event():
    event = Event(
        id=2,
        description='Ski|Snowboarding Day Trip to Camelback Mountain Jan 10',
        rental=32,
        lift=51,
        lesson=63,
        bus=42,
        ticket_num=55
    )
    app.db.session.merge(event)
    app.db.session.commit()


@manager.command
def update_ticket():
    ticket = Ticket(
        id=2,
        description='Ski|Snowboarding Day Trip to Camelback Mountain Jan 10',
        lift=56,
        snowboard=36,
        ski=36
    )
    app.db.session.merge(ticket)
    app.db.session.commit()


if __name__ == "__main__":
    manager.run()
