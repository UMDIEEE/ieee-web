from flask import Flask, render_template, redirect, url_for
from flask.ext.security import login_required, current_user, roles_accepted
from flask_menu import register_menu

from IEEETestbankApp import app
from IEEETestbankApp.views.admin.admin import check_admin
from IEEETestbankApp.views.defaults import get_default_template_kwargs

@app.route('/admin/dashboard')
@register_menu(app, 'main.admin.dashboard', 'Dashboard', order = 0, visible_when = check_admin)
@roles_accepted('Administrator')
def admin_dashboard():
    template_kwargs = get_default_template_kwargs()
    return render_template('admin/demo.html', **template_kwargs)
