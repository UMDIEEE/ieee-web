from flask import Flask, render_template
from flask.ext.security import login_required, current_user
from flask_menu import register_menu
from IEEETestbankApp import app

# Browse page

# Views
@app.route('/browse')
@register_menu(app, 'main.browse', 'Browse', order = 1)
def browse():
    return render_template('search.html', user = current_user)

