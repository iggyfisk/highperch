"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)
# Todo: build environment
app.secret_key = "debug"
import perchweb.views
