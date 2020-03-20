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
import geoip


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
        try:
            current_app.logger.error(
                'Attempted to log to Slack, but no hook environment variable is present')
        except RuntimeError:
            pass


def upload_to_slack(replay_name, file_bytes):
    if environ.get('HIGHPERCH_SLACK_BOT_TOKEN'):
        bot_token = environ.get('HIGHPERCH_SLACK_BOT_TOKEN')
        filename = replay_name + '.w3g'
        file_obj = {'file': (filename, file_bytes, 'w3g')}
        payload = {
            "filename": filename,
            "token": bot_token,
            "channels": ['#highperch-alerts'],
            "title": replay_name
        }
        post("https://slack.com/api/files.upload", params=payload, files=file_obj)
    else:
        current_app.logger.error(
            'Attempted to upload file to Slack, but no bot token environment variable is present')


def format_ip_addr(ip_addr):
    country_code = geoip.lookup_country(ip_addr)['code']
    city, subdivision = geoip.lookup_city(ip_addr)[0], geoip.lookup_city(ip_addr)[1]
    return f'{ip_addr} ({city}, {subdivision}, {country_code})'

