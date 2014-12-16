# -*- coding: utf-8 -*-

from flask.ext.script import Manager
from start import create_app
from settings import DEV as ENV
from flask.ext.migrate import Migrate, MigrateCommand
from start.models import Event

app = create_app(ENV)
manager = Manager(app)

migrate = Migrate(app, app.db)
manager.add_command('db', MigrateCommand)


@manager.command
def update_event():
    event = Event(
        id=1,
        description='Ski|Snowboarding Day Trip to Windham Mountain Dec 20',
        rental=32,
        lift=40,
        lesson=24,
        bus=30,
        ticket_num=24
    )
    app.db.session.merge(event)
    app.db.session.commit()


if __name__ == "__main__":
    manager.run()
