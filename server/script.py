# -*- coding: utf-8 -*-

from flask.ext.script import Manager
from start import create_app
from settings import PROD as ENV
from flask.ext.migrate import Migrate, MigrateCommand
from start.models import Event, Order

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
        lift=45,
        lesson=30,
        bus=45,
        ticket_num=21
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
        print '%s %s, %s, %s, %s, %s' % (order.first_name, order.last_name, order.lift, order.rental, order.location, order.total)


if __name__ == "__main__":
    manager.run()
