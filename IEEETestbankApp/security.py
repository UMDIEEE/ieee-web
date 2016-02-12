from flask.ext.security import Security, SQLAlchemyUserDatastore

from IEEETestbankApp import app
from IEEETestbankApp.models.db import db
from IEEETestbankApp.models.auth import User, Role
from IEEETestbankApp.forms import *
from IEEETestbankApp import cas

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, confirm_register_form=UMDConfirmRegisterForm)

@security.register_context_processor
def security_register_processor():
    if cas:
        return dict(username=cas.username)
    else:
        return dict()
