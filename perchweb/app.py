"""
The flask application package.
"""

from os import environ, path
from glob import glob
from hashlib import md5
import base64
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

# Cache bust CSS and JS which may have changed, quick n dirty
mutable_static = glob(path.join(app.root_path, 'static/style', '*.css')) + \
    glob(path.join(app.root_path, 'static/script', '*.js'))

hash_obj = md5(open(mutable_static[0], 'rb').read())
for static_file in mutable_static[1:]:
    hash_obj.update(open(static_file, 'rb').read())
app.config['STATIC_HASH'] = base64.urlsafe_b64encode(hash_obj.digest()).decode('ascii')[:-2]

if __name__ == "__main__":
    app.run()
