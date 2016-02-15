from flask import Flask, render_template, url_for, redirect
from flask.ext.cas import login_required as cas_login_required
from flask.ext.security.utils import login_user
import flask.ext.security.views
from flask_menu import Menu

from IEEETestbankApp import app, cas, menu
from IEEETestbankApp.models.auth import User, Role
from IEEETestbankApp.models.db import db, initDatabase
from IEEETestbankApp.security import *

'''
@app.before_first_request
def _build_login_link():
    print("Current: %s (%s)" % (str(Menu.root()), Menu.root().text))
    print("CHILDREN: %s" % str(Menu.root().submenu))
    print("CHILDREN: %s" % str(Menu.root().children))
    print(Menu.root().children[0].text)
    login_submenu = Menu.root().submenu("security.login")
    login_submenu.register("security.login", "Login", 10)
    
    logout_submenu = Menu.root().submenu("security.logout")
    logout_submenu.register("security.logout", "Login", 10)
'''

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
