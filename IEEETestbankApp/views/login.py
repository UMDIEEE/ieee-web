from flask import Flask, render_template, url_for, redirect
from flask.ext.cas import login_required as cas_login_required
from flask.ext.security.utils import login_user

from IEEETestbankApp import app, cas
from IEEETestbankApp.models.auth import User, Role
from IEEETestbankApp.models.db import db, initDatabase
from IEEETestbankApp.security import *

@app.route('/umdlogin')
@cas_login_required
def login_umd():
    print("Login succeeded: username = '%s', attributes='%s'" % (cas.username, str(cas.attributes)))
    initDatabase()
    user_search = User.query.filter_by(username=cas.username).first()
    target_user = user_datastore.find_user(username = cas.username)
    print(user_search)
    print(target_user)
    
    if user_search and target_user:
        print("User %s exists, proceeding to login." % cas.username)
        login_user(target_user)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        print("User %s does NOT exist, proceeding to registration." % cas.username)
        return redirect(url_for('umdregister'))
