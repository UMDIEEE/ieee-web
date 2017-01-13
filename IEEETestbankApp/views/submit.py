from flask import Flask, render_template
from flask.ext.security import login_required, current_user
from flask_menu import register_menu
from IEEETestbankApp import app
from IEEETestbankApp.views.defaults import get_default_template_kwargs

# Browse page

# Views
@app.route('/submit')
@register_menu(app, 'main.submit', 'Submit', order = 2)
def submit():
    template_kwargs = get_default_template_kwargs()
    return render_template('search.html', **template_kwargs)

