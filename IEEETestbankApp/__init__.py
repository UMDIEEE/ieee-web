import os

from flask import Flask
from flask.ext.cas import CAS

app = Flask(__name__)
cas = CAS(app, '/cas')

# Create app
app.config.from_pyfile('config.py', silent=True)
app.config.from_pyfile(os.path.join(app.instance_path, 'config.py'))

import IEEETestbankApp.security
import IEEETestbankApp.models
import IEEETestbankApp.views
