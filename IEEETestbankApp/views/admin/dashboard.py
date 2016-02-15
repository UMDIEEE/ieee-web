from flask import Flask, render_template, redirect, url_for
from flask.ext.security import login_required, current_user, roles_accepted
from flask_menu import register_menu

from IEEETestbankApp import app
from IEEETestbankApp.views.admin.admin import check_admin

@app.route('/admin/dashboard')
@register_menu(app, 'main.admin.dashboard', 'Dashboard', order = 0, visible_when = check_admin)
@roles_accepted('Administrator')
def admin_dashboard():
    return render_template('admin/demo.html', user = current_user)