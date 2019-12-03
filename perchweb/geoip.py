"""GeoIP lookups"""

import geoip2.database
from flask import Flask
from filepaths import get_path

app = Flask(__name__)

with app.app_context():
    geoip_country_db = geoip2.database.Reader(get_path('resource/GeoLite2-Country.mmdb'))
    geoip_city_db = geoip2.database.Reader(get_path('resource/GeoLite2-City.mmdb'))

def lookup_country(ip_addr):
    try:
        response = geoip_country_db.country(ip_addr)
        result = {'code': response.country.iso_code,
                  'name': response.country.name}
        return result
    except Exception as e:
        return {'code': "xx", 'name': "unknown"}


def lookup_city(ip_addr):
    try:
        response = geoip_city_db.city(ip_addr)
        return (response.city.name, response.subdivisions.most_specific.iso_code)
    except Exception as e:
        return 'unknown'
