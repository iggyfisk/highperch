"""Administration functions"""

from os import environ
from werkzeug.security import check_password_hash
import geoip2.database


def validate_admin_hash(token):
    return check_password_hash(environ.get('HIGHPERCH_ADMIN_HASH'), token)


def check_if_admin(cookies):
    if 'HP_ADMIN_TOKEN' in cookies:
        print("admin", cookies['HP_ADMIN_TOKEN'] == environ.get('HIGHPERCH_ADMIN_HASH'))
        return cookies['HP_ADMIN_TOKEN'] == environ.get('HIGHPERCH_ADMIN_HASH')
    else:
        return False


def geoip_country(ip_addr):
    reader = geoip2.database.Reader('static/geoip/GeoLite2-Country.mmdb')
    try:
        response = reader.country(ip_addr)
        result = {'code': response.country.iso_code, 'name': response.country.name}
        return result
    except geoip2.errors.AddressNotFoundError:
        return {'code': "xx", 'name': "unknown"}
    except Exception as e:
        return {'code': "xx", 'name': "unknown"}


def geoip_city(ip_addr):
    reader = geoip2.database.Reader('static/geoip/GeoLite2-City.mmdb')
    try:
        return reader.city.name(ip_addr)
    except geoip2.errors.AddressNotFoundError:
        return "unknown"
