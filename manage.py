from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import os

from IEEETestbankApp import app
from IEEETestbankApp.models.db import db
from IEEETestbankApp.models.auth import *

with app.app_context():
    app.config.from_object(os.environ.get('APP_SETTINGS'))
    
    migrate = Migrate(app, db)
    manager = Manager(app)
    
    manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    with app.app_context():
        manager.run()
