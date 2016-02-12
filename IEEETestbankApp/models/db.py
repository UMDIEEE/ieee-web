from flask.ext.sqlalchemy import SQLAlchemy
import sqlalchemy_utils

from IEEETestbankApp import app
import IEEETestbankApp.models

global run_once
run_once = False

def initDatabase():
    global run_once
    
    if not run_once:
        run_once = True
        if not sqlalchemy_utils.functions.database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
            sqlalchemy_utils.functions.create_database(app.config['SQLALCHEMY_DATABASE_URI'])
    
    print("Initializing database!")
    db.create_all()

db = SQLAlchemy(app)
