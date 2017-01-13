from flask import Flask, render_template
from flask.ext.security import login_required, current_user
from flask_menu import register_menu
from IEEETestbankApp import app
from IEEETestbankApp.views.defaults import get_default_template_kwargs

# Home page

# Views
@app.route('/')
@register_menu(app, 'main.home', 'Home', order = 0)
def home():
    template_kwargs = get_default_template_kwargs()
    return render_template('search.html', **template_kwargs)

@app.route('/debug')
def debug():
    raise
