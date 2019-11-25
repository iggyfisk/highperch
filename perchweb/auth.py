"""Authentication functions"""

from os import environ
from functools import wraps
from werkzeug.security import check_password_hash
from flask import request, redirect, make_response, abort

# Todo: Set env_hash_key for everyone's development environment so we can remove these fallbacks

cookie_key = 'HP_ADMIN_TOKEN'
env_hash_key = 'HIGHPERCH_ADMIN_HASH'


def validate_admin_hash(token):
    if env_hash_key in environ:
        return check_password_hash(environ.get(env_hash_key), token)

    # Todo: aaah mega bad but I need to add some admin stuff
    return True


def check_if_admin(cookies):
    if cookie_key in cookies:
        return cookies[cookie_key] == environ.get(env_hash_key, 'Development Token')
    else:
        return False


def admin_only(func):
    """ Decorator for admin-only routes """
    @wraps(func)
    def decorated_route(*args, **kwargs):
        if not check_if_admin(request.cookies):
            abort(403)

        return func(*args, **kwargs)

    return decorated_route


def login(token, redirect_url):
    """ Validates the given token and returns a response with auth cookies if valid, otherwise None """
    if validate_admin_hash(token):
        response = make_response(redirect(redirect_url))
        response.set_cookie(cookie_key, value=environ.get(env_hash_key, 'Development Token'),
                            max_age=7305*86400,
                            secure=(environ.get('HIGHPERCH_ENVIRONMENT',
                                                'development') == "production"),
                            httponly=True,
                            samesite='Strict')
        return response
    return None


def logout(redirect_url):
    """ Return a response that clears auth cookies """
    response = make_response(redirect(redirect_url))
    response.set_cookie(cookie_key, '', expires=0)
    return response


def add_auth_attributes():
    """ Populates templates with standard auth attributes """
    return {'is_admin': check_if_admin(request.cookies)}
