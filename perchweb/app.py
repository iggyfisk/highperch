"""
The flask application package.
"""

from os import environ, path
from glob import glob
from hashlib import md5
import base64
from flask import Flask
from views import routes as public_routes
from admin import routes as admin_routes
from templatefilters import register
from replaydb import close_connection as close_replaydb
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
register(app.jinja_env)
app.register_blueprint(public_routes)
app.register_blueprint(admin_routes)


# Not a fan of not having this logic contained to whoever needs cleanup but too much time wasted
@app.teardown_appcontext
def cleanup(error):
    """ End of request, commit all transactions and close connections """
    close_replaydb()
    if error is not None:
        # Todo: Log
        print(error)


app.config.from_pyfile(path.join(app.root_path, 'app.cfg'))

if environ.get('HIGHPERCH_ENVIRONMENT') == "production":
    app.secret_key = environ.get('HIGHPERCH_FLASK_KEY')
    app.config.update(SESSION_COOKIE_SECURE=True,
                      SESSION_COOKIE_HTTPONLY=True,
                      SESSION_COOKIE_SAMESITE='Strict')
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
