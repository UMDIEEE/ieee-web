from flask import Flask, render_template
from flask.ext.cas import login_required as cas_login_required

from IEEETestbankApp import app, cas
from IEEETestbankApp.models.auth import User, Role

@app.route('/umdlogin')
@cas_login_required
def login_umd():
    print("Login succeeded: username = '%s', attributes='%s'" % (cas.username, str(cas.attributes)))
    print(User.query.filter_by(username=cas.username).first())
    if User.query.filter_by(username=cas.username).first():
        print("User %s exists, proceeding to login." % cas.username)
    else:
        print("User %s does NOT exist, proceeding to registration." % cas.username)
    
    return render_template('search.html')
