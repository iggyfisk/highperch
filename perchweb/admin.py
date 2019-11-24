"""Administration functions"""

from os import environ
from werkzeug.security import check_password_hash


def validate_admin_hash(token):
    return check_password_hash(environ.get('HIGHPERCH_ADMIN_HASH'), token)


def check_if_admin(cookies):
    if 'HP_ADMIN_TOKEN' in cookies:
        return cookies['HP_ADMIN_TOKEN'] == environ.get('HIGHPERCH_ADMIN_HASH')
    else:
        return False