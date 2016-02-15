from flask import Flask, render_template
from flask.ext.security import login_required, current_user
from flask_menu import register_menu
from IEEETestbankApp import app

# Home page

# Views
@app.route('/')
@register_menu(app, 'main.home', 'Home', order = 0)
def home():
    return render_template('search.html', user = current_user)

@app.route('/debug')
def debug():
    raise
