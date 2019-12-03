"""
The flask application package.
"""

from os import environ, path
from glob import glob
from hashlib import md5
import base64
import logging
import geoip2.database
from logging.config import fileConfig
from werkzeug.exceptions import HTTPException, InternalServerError
from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask, request, redirect
from views import routes as public_routes
from admin import routes as admin_routes
from templatefilters import register
from replaydb import close_connection as close_replaydb
from perchlogging import log_to_slack, format_traceback, sanitize_cookie
from handler import standard_page


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
register(app.jinja_env)
app.register_blueprint(public_routes)
app.register_blueprint(admin_routes)

log_cfg = 'perchweb/logging.cfg'

if path.exists(log_cfg):
    fileConfig(log_cfg)
else:
    logging.basicConfig(level=logging.DEBUG)

geoip_country_reader = geoip2.database.Reader(path.join(app.root_path, 'resource/GeoLite2-Country.mmdb'))
geoip_city_reader = geoip2.database.Reader(path.join(app.root_path, 'resource/GeoLite2-City.mmdb'))

# Not a fan of not having this logic contained to whoever needs cleanup but too much time wasted
@app.teardown_appcontext
def cleanup(error):
    """ End of request, commit all transactions and close connections """
    close_replaydb()


@app.errorhandler(405)
def method_not_allowed(error):
    error_string = ('\nRequest IPaddr: ' + request.remote_addr)
    error_string += ('\nURL: ' + request.url)
    error_string += ('\n----- begin headers -----\n\n' +
                     sanitize_cookie(str(request.headers)))
    error_string += ('----- end headers -----\nTraceback:\n')
    error_string += format_traceback(error)
    app.logger.error(error_string)
    log_to_slack(
        'ERROR', f"405 [{error.__class__.__name__}] \n{error_string}")
    return redirect("/", code=302)


@app.errorhandler(Exception)
def internal_error(error):
    if isinstance(error, HTTPException) and error.code < 500:
        return error.get_response()
    error_string = ('\nRequest IPaddr: ' + request.remote_addr)
    error_string += ('\nURL: ' + request.url)
    error_string += ('\n----- begin headers -----\n\n' +
                     sanitize_cookie(str(request.headers)))
    error_string += ('----- end headers -----\nTraceback:\n')
    error_string += format_traceback(error)
    app.logger.error(error_string)
    log_to_slack(
        'ERROR', f"500 [{error.__class__.__name__}] \n{error_string}")
    return (error if isinstance(error, HTTPException) else InternalServerError()).get_response()


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
app.config['STATIC_HASH'] = base64.urlsafe_b64encode(
    hash_obj.digest()).decode('ascii')[:-2]

if __name__ == "__main__":
    app.run()

if __name__ != "__main__":
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
