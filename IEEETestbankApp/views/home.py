from flask import Flask, render_template
from flask.ext.security import login_required, current_user
from IEEETestbankApp import app

# Home page

# Views
@app.route('/')
def home():
    return render_template('index.html', user = current_user)

