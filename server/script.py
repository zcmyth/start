# -*- coding: utf-8 -*-

from flask.ext.script import Manager
from start import create_app
from settings import DEV as ENV
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(ENV)
manager = Manager(app)

migrate = Migrate(app, app.db)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
