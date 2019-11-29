"""
Custom logging functions
"""

from os import environ
from json import dumps
from re import sub
import traceback
from admin import geoip_city, geoip_country
from flask import current_app, request
from requests import post


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


def format_ip_addr(ip_addr):
    failed_country_code = geoip_country(ip_addr)['code']
    return f'{ip_addr} ({failed_country_code} / {geoip_city(request.remote_addr)})'
