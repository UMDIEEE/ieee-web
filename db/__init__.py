from flask.ext.sqlalchemy import SQLAlchemy
import sqlalchemy_utils

from IEEETestbankApp import app, models

db = SQLAlchemy(app)

if not sqlalchemy_utils.functions.database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
    sqlalchemy_utils.functions.create_database(app.config['SQLALCHEMY_DATABASE_URI'])

db.create_all()
