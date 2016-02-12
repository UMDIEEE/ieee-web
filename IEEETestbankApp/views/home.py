from flask import Flask, render_template
from flask.ext.security import login_required
from IEEETestbankApp import app

# Home page

# Views
@app.route('/')
def home():
    return render_template('index.html')

