"""
Custom logging functions
"""

from os import environ
from json import dumps
from re import sub
import traceback
from flask import current_app, request
from requests import post
from filepaths import get_path
import geoip2.database


def sanitize_cookie(headers):
    return sub('pbkdf2:sha256:\d{6}\$\w{8}\$[0-9a-f]{64}', '[SANITIZED-COOKIE]', headers)


def format_traceback(exception_object):
    return ''.join(traceback.format_tb(exception_object.__traceback__))


def log_to_slack(level, log_message):
    if environ.get('HIGHPERCH_SLACK_HOOK'):
        hook_url = environ.get('HIGHPERCH_SLACK_HOOK')
        payload = {
            'username': 'Flask Alerts',
            'icon_emoji': ':tower:',
            'text': f'```[{level}] {str(log_message)}```'
        }
        post(hook_url, data=dumps(payload), headers={
            'Content-Type': 'application/json'})
    else:
        current_app.logger.error(
            'Attempted to log to Slack, but no hook environment variable is present')


def geoip_country(ip_addr):
    reader = geoip2.database.Reader(get_path('resource/GeoLite2-Country.mmdb'))
    try:
        response = reader.country(ip_addr)
        result = {'code': response.country.iso_code,
                  'name': response.country.name}
        return result
    except Exception as e:
        return {'code': "xx", 'name': "unknown"}


def geoip_city(ip_addr):
    reader = geoip2.database.Reader(get_path('resource/GeoLite2-City.mmdb'))
    try:
        response = reader.city(ip_addr)
        return (response.city.name, response.subdivisions.most_specific.iso_code)
    except Exception as e:
        return 'unknown'


def format_ip_addr(ip_addr):
    country_code = geoip_country(ip_addr)['code']
    city, subdivision = geoip_city(ip_addr)[0], geoip_city(ip_addr)[1]
    return f'{ip_addr} ({city}, {subdivision}, {country_code})'

