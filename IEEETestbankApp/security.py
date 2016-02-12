from flask.ext.security import Security, SQLAlchemyUserDatastore

from IEEETestbankApp import app
from IEEETestbankApp.models.db import db
from IEEETestbankApp.models.auth import User, Role

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
