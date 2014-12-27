# -*- coding: utf-8 -*-

from flask.ext.script import Manager
from start import create_app
from settings import DEV as ENV
from flask.ext.migrate import Migrate, MigrateCommand
from start.models import Event, Order

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


@manager.option('-i', '--id', help='event id')
def event(id):
    orders = Order.query.filter_by(
        event_id=id,
        status='PAID'
    ).all()
    print 'name, lift, rental, location, total'
    for order in orders:
        print '%s %s, %s, %s, %s, %s' % (order.first_name, order.last_name,
                                         order.lift, order.rental,
                                         order.location, order.total)


if __name__ == "__main__":
    manager.run()
