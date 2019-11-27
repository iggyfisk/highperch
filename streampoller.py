""" Keeps an up to date record of active boystreams for web display,
    notifies Slack on changes """

import sqlite3
import sys
from os import environ
import requests


db = None


def get_connection():
    global db
    if db is None:
        db = sqlite3.connect('streams.db')
        db.row_factory = sqlite3.Row
    return db


def commit():
    global db
    if db is not None:
        db.commit()
        db.close()


def query(query_text, args=(), one=False):
    """ Run query_text with args against the stream db, one=True for a single result row """
    cursor = get_connection().execute(query_text, args)
    results = cursor.fetchall()
    cursor.close()
    return (results[0] if results else None) if one else results


def notify_slack(message):
    webhook_url = environ.get('HIGHPERCH_STREAM_WEBHOOK', None)
    if not webhook_url:
        raise RuntimeError('HIGHPERCH_STREAM_WEBHOOK not set')

    payload = {'text': message}
    requests.post(webhook_url, json=payload)


def notify_slack_twitch(url, name, game, status):
    livestreamer_url = 'https://gist.github.com/iggyfisk/bf381eb0c566560a7a84#file-livestreamer-md'

    content = f'*{game}*: _{status}_' if status else f'*{game}*'
    message = f'{url} is streaming {content}\n<twitch://stream/{name}|Twitch app> | <livestreamer://{url}|Livestreamer> <{livestreamer_url}|*?*>'
    notify_slack(message)


if __name__ == "__main__":
    client_id = environ.get('HIGHPERCH_TWITCH_CLIENT_ID', None)
    if not client_id:
        print('HIGHPERCH_TWITCH_CLIENT_ID not set')
        sys.exit(1)

    base_url = 'https://api.twitch.tv/kraken/streams/'
    headers = {'Accept': 'application/vnd.twitchtv.v5+json',
               'Client-ID': client_id}

    twitch_streams = query('SELECT TwitchID, Streaming, Name FROM Twitch')

    for stream in twitch_streams:
        twitch_id = stream['TwitchID']
        twitch_data = requests.get(
            f'{base_url}{twitch_id}', headers=headers).json()
        current_stream = twitch_data['stream'] if 'stream' in twitch_data else None

        if current_stream is None:
            if stream['Streaming'] == 1:
                # Stream went from on to off
                query('UPDATE Twitch SET Streaming = 0 WHERE TwitchID = ?', (twitch_id,))
                try:
                    notify_slack(
                        f'{stream["Name"]} is no longer streaming on Twitch')
                except Exception as err:
                    # Todo: log
                    print(err)
            continue

        name = current_stream['channel']['name']
        url = current_stream['channel']['url']
        game = current_stream['game']
        status = current_stream['channel']['status']

        query('''UPDATE Twitch SET Streaming = 1, Name = ?, URL = ?, Game = ?,
            Status = ? WHERE TwitchID = ?''', (name, url, game, status, twitch_id))

        if stream['Streaming'] == 0:
            # Stream went from off to on
            try:
                notify_slack_twitch(url, name, game, status)
            except Exception as err:
                # Todo: log
                print(err)
    commit()
