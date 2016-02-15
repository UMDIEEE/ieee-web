from flask import Flask, render_template, redirect, url_for
from flask.ext.security import login_required, current_user, roles_accepted
from flask_menu import register_menu

from IEEETestbankApp import app
from IEEETestbankApp.views.admin.admin import check_admin

@app.route('/admin')
@register_menu(app, 'main.admin', 'Admin', order = 3, visible_when = check_admin)
@roles_accepted('Administrator')
def admin():
    return redirect(url_for('admin_dashboard'))
