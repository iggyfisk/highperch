""" Administration routes and utilities """

import geoip2.database
from flask import Blueprint, url_for, request, redirect, flash
from auth import admin_only, logout as auth_logout
from handler import admin_page
from replaydb import save_chatlog, delete_replay as dbdelete_replay
from filepaths import get_path

routes = Blueprint('admin', __name__)


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


@routes.route('/logout')
def logout():
    """ Log out and go back to index as a member of the general public """
    return auth_logout(url_for('views.index'))


@routes.route('/footer/<int:replay_id>', methods=['POST'])
@admin_only
def add_footer(replay_id):
    """ Add a sick chatlog to the footer rotation """
    chat = request.form['chat'].strip()
    save_chatlog(replay_id, chat)
    flash('Chatlog added to footer rotation')

    return redirect(url_for('views.view_replay', replay_id=replay_id))


@routes.route('/replay/<int:replay_id>/delete', methods=['POST'])
@admin_only
def delete_replay(replay_id):
    """ Permanently deletes a replay and related objects from the system """
    redirect_url = url_for('views.index') if dbdelete_replay(
        replay_id) else url_for('views.view_replay', replay_id=replay_id)

    return redirect(redirect_url)
