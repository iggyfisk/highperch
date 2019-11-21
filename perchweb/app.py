"""
The flask application package.
"""

from os import environ, path
from flask import Flask
from views import routes

from replaydb import close_connection as close_replaydb

app = Flask(__name__)
app.register_blueprint(routes)

# Not a fan of not having this logic contained to whoever needs cleanup but too much time wasted
@app.teardown_appcontext
def cleanup(e):
    close_replaydb()


app.config.from_pyfile(path.join(app.root_path, 'app.cfg'))

if environ.get('HIGHPERCH_ENVIRONMENT') == "production":
    app.secret_key = environ.get('HIGHPERCH_FLASK_KEY')
else:
    app.secret_key = 'debug'

if __name__ == "__main__":
    app.run()
