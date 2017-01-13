from flask import Flask, render_template, redirect, url_for
from flask.ext.security import login_required, current_user, roles_accepted
from flask_menu import register_menu

from IEEETestbankApp import app
from IEEETestbankApp.views.admin.admin import check_admin
from IEEETestbankApp.models.auth import User, Role

def translate_roles(roles):
    return ", ".join([r.name for r in roles])

# Users
@app.route('/admin/users')
@register_menu(app, 'main.admin.users', 'Users', order = 2, visible_when = check_admin)
@roles_accepted('Administrator')
def admin_users():
    template_kwargs = get_default_template_kwargs()
    return render_template('admin/demo.html', **template_kwargs)

@app.route('/admin/users/list')
@register_menu(app, 'main.admin.users.list', 'User List', order = 0, visible_when = check_admin)
@roles_accepted('Administrator')
def admin_users_list():
    template_kwargs = get_default_template_kwargs()
    return render_template('admin/users_list.html',
        user_list = User.query.all(),
        translate_roles = translate_roles,
        **template_kwargs)
