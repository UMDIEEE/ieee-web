import os

from flask import Flask, render_template, redirect, url_for, request, flash
from flask.ext.security import login_required, current_user, roles_accepted
from flask_menu import register_menu

from IEEETestbankApp import app
from IEEETestbankApp.views.admin.admin import check_admin
from IEEETestbankApp.models.auth import Config
from IEEETestbankApp.models.db import db
from IEEETestbankApp.forms import TestbankSettingsForm
from IEEETestbankApp.views.credhelper import fetch_latest_cred, store_cred

from apiclient import discovery
from oauth2client import client

import httplib2
import traceback

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

@app.route('/admin/testbank/settings', methods=['GET', 'POST'])
@register_menu(app, 'main.admin.testbank.settings', 'Testbank Settings', order = 3, visible_when = check_admin)
@roles_accepted('Administrator')
def admin_testbank_settings():
    form = TestbankSettingsForm(request.form)
    
    config_gdrive_cred = Config.query.filter_by(name='gdrive_oauth2_credentials').first()
    config_gdrive_folder = Config.query.filter_by(name='gdrive_folder').first()
    
    if request.method == 'POST' and form.validate():
        flash("Setttings updated!")
        if config_gdrive_folder != None:
            config_gdrive_folder.value = form.gdrive_folder.data
            db.session.commit()
        else:
            config_gdrive_folder = Config(name = 'gdrive_folder',
                            value = form.gdrive_folder.data,
                            description = "Google Drive Folder for Tests")
            db.session.add(config_gdrive_folder)
            db.session.commit()
    
    if config_gdrive_folder != None:
        form.gdrive_folder.data = config_gdrive_folder.value
    
    print("[testbank.py] config_gdrive_cred = %s" % str(config_gdrive_cred))
    
    if config_gdrive_cred:
        try:
            credentials = fetch_latest_cred(config_gdrive_cred.value)
        except (ValueError, client.HttpAccessTokenRefreshError):
            flash("Could not decode credentials, erasing.")
            config_gdrive_user = None
            db.session.delete(config_gdrive_cred)
            db.session.commit()
            config_gdrive_cred = None
            
            return render_template('admin/testbank_settings.html', user = current_user,
                config_gdrive_cred = config_gdrive_cred, config_gdrive_user = config_gdrive_user,
                testbank_settings_form = form)
        try:
            http_auth = credentials.authorize(httplib2.Http())
            people_service = discovery.build('people', 'v1', http_auth)
            linked_acct_info = people_service.people().get(resourceName='people/me').execute()
            linked_acct_info_name = linked_acct_info.get('names')[0].get("displayName")
            linked_acct_info_email = linked_acct_info.get('emailAddresses')[0].get("value")
            config_gdrive_user = [ linked_acct_info_name, linked_acct_info_email ]
        except:
            flash(traceback.format_exc())
            config_gdrive_user = None
    else:
        config_gdrive_user = None
    
    return render_template('admin/testbank_settings.html', user = current_user,
        config_gdrive_cred = config_gdrive_cred, config_gdrive_user = config_gdrive_user,
        testbank_settings_form = form)

@app.route('/admin/testbank/gdrive_auth')
def gdrive_auth():
    config_gdrive_cred = Config.query.filter_by(name='gdrive_oauth2_credentials').first()
    if not config_gdrive_cred:
        return redirect(url_for('gdrive_oauth2callback'))
    
    try:
        credentials = fetch_latest_cred(config_gdrive_cred.value)
    except ValueError:
        flash("Could not decode credentials, erasing.")
        db.session.delete(config_gdrive_cred)
        db.session.commit()
        config_gdrive_cred = None
        
        return redirect(url_for('admin_testbank_settings'))
    
    if credentials.access_token_expired:
        return redirect(url_for('gdrive_deauth'))
    else:
        return redirect(url_for('admin_testbank_settings'))

@app.route('/admin/testbank/gdrive_deauth')
def gdrive_deauth():
    config_gdrive_cred = Config.query.filter_by(name='gdrive_oauth2_credentials').first()
    if not config_gdrive_cred:
        flash("No Google Drive account is linked at the moment.")
        return redirect(url_for('admin_testbank_settings'))
    
    credentials = fetch_latest_cred(config_gdrive_cred.value)
    
    try:
        credentials.revoke(httplib2.Http())
    except:
        flash("Could not revoke credentails! Assuming credentials are already revoked. Reason: " + traceback.format_exc())
    
    db.session.delete(config_gdrive_cred)
    db.session.commit()
    
    flash("Google Drive account unlinked successfully.")
    return redirect(url_for('admin_testbank_settings'))

@app.route('/admin/testbank/gdrive_oauth2callback')
def gdrive_oauth2callback():
    flow = client.flow_from_clientsecrets(
        os.path.join(app.instance_path, 'client_secrets.json'),
        scope='https://www.googleapis.com/auth/drive email profile',
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
        store_cred(credentials)
        return redirect(url_for('gdrive_auth'))
