"""
Runs the code in web/ with a development server
"""

from os import environ
from perchweb import app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    if environ.get('HIGHPERCH_ENVIRONMENT') == "production":
        app.secret_key = environ.get('HIGHPERCH_FLASK_KEY')
        app.config['DEBUG'] = False
    else:
        app.secret_key = 'debug'
    app.run(HOST, PORT, debug=True)
