import os

from flask import Flask, render_template, redirect, url_for, request
from flask.ext.security import login_required, current_user, roles_accepted
from flask_menu import register_menu

from IEEETestbankApp import app
from IEEETestbankApp.views.admin.admin import check_admin
from IEEETestbankApp.models.auth import Config
from IEEETestbankApp.models.db import db

from apiclient import discovery
from oauth2client import client

@app.route('/admin/testbank')
@register_menu(app, 'main.admin.testbank', 'Testbank', order = 1, visible_when = check_admin)
@roles_accepted('Administrator')
def admin_testbank():
    return render_template('admin/demo.html', user = current_user)

@app.route('/admin/testbank/approve')
@register_menu(app, 'main.admin.testbank.approve', 'Approve Exams', order = 1, visible_when = check_admin)
@roles_accepted('Administrator')
def admin_testbank_approve():
    return render_template('admin/demo.html', user = current_user)

@app.route('/admin/testbank/edit')
@register_menu(app, 'main.admin.testbank.edit', 'Edit Exams', order = 2, visible_when = check_admin)
@roles_accepted('Administrator')
def admin_testbank_edit():
    return render_template('admin/demo.html', user = current_user)

@app.route('/admin/testbank/settings')
@register_menu(app, 'main.admin.testbank.settings', 'Testbank Settings', order = 3, visible_when = check_admin)
@roles_accepted('Administrator')
def admin_testbank_settings():
    config_gdrive_cred = Config.query.filter_by(name='gdrive_oauth2_credentials').first()
    return render_template('admin/testbank_settings.html', user = current_user, cred = config_gdrive_cred)

@app.route('/admin/testbank/gdrive_auth')
def gdrive_auth():
    config_gdrive_cred = Config.query.filter_by(name='gdrive_oauth2_credentials').first()
    if not config_gdrive_cred:
        return redirect(url_for('gdrive_oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(config_gdrive_cred.value)
    if credentials.access_token_expired:
        return redirect(url_for('gdrive_oauth2callback'))
    else:
        return redirect(url_for('admin_testbank_settings'))

@app.route('/admin/testbank/gdrive_oauth2callback')
def gdrive_oauth2callback():
    flow = client.flow_from_clientsecrets(
        os.path.join(app.instance_path, 'client_secrets.json'),
        scope='https://www.googleapis.com/auth/drive',
        redirect_uri=url_for('gdrive_oauth2callback', _external=True)
    )
    flow.params['include_granted_scopes'] = 'true'
    flow.params['access_type'] = 'offline'
    if 'code' not in request.args:
        auth_uri = flow.step1_get_authorize_url()
        return redirect(auth_uri)
    else:
        auth_code = request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        new_cred = Config(name = 'gdrive_oauth2_credentials',
                            value = credentials.to_json(),
                            description = "IEEE@UMD Testbank <-> Google Drive Credentials")
        db.session.add(new_cred)
        db.session.commit()
        return redirect(url_for('gdrive_auth'))
