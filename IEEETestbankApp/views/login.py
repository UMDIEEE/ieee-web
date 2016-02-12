from flask import Flask, render_template, url_for, redirect, request
from flask.ext.cas import login_required as cas_login_required
from flask.ext.security.utils import login_user

from IEEETestbankApp import app, cas
from IEEETestbankApp.models.auth import User, Role
from IEEETestbankApp.forms import *
from IEEETestbankApp.security import *

@app.route('/umdlogin')
@cas_login_required
def login_umd():
    print("Login succeeded: username = '%s', attributes='%s'" % (cas.username, str(cas.attributes)))
    
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
    
    return render_template('search.html')

@app.route('/umdregister', methods=['GET', 'POST'])
@cas_login_required
def umdregister():
    form = UMDConfirmRegisterForm(request.form)
    print("Login succeeded: username = '%s', attributes='%s'" % (cas.username, str(cas.attributes)))
    user_search = User.query.filter_by(username=cas.username).first()
    target_user = user_datastore.find_user(username = cas.username)
    print(user_search)
    
    if request.method == 'POST' and form.validate():
        print("Form validated! Creating user...")
        new_user = user_datastore.create_user(username = cas.username,
                                    first_name = form.first_name.data,
                                    last_name = form.last_name.data,
                                    major = form.major.data,
                                    grad_semester = form.grad_semester.data,
                                    grad_year = form.grad_year.data
                                  )
        login_user(new_user)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        if user_search and target_user:
            print("User %s exists, proceeding to login." % cas.username)
            return redirect(url_for('umdlogin'))
        else:
            print("User %s does NOT exist, proceeding to registration." % cas.username)
    
    return render_template('security/register_user.html', register_user_form = form, username = cas.username)
