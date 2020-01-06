""" Administration routes and utilities """

from collections import defaultdict
from datetime import datetime
from zipfile import ZipFile, ZIP_DEFLATED
from os import path, remove
from glob import glob
from flask import Blueprint, url_for, request, redirect, flash, send_from_directory, send_file
from werkzeug.utils import secure_filename
from auth import admin_only, logout as auth_logout
from handler import admin_page
from replaydb import get_all_replays, get_all_uploader_ips, save_chatlog, \
    delete_replay as dbdelete_replay, edit_replay as dbedit_replay
from peep import save_pic
from filepaths import get_db, get_temp, get_replay_data

routes = Blueprint('admin', __name__)


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


@routes.route('/replay/<int:replay_id>/edit', methods=['POST'])
@admin_only
def edit_replay(replay_id):
    """ Changes whatever replay information in the DB that could reasobly be changed """
    replay_name = request.form['name'].strip()
    if (len(replay_name) < 6 or len(replay_name) > 50):
        flash('Bad name')
    else:
        dbedit_replay(replay_id, replay_name)

    return redirect(url_for('views.view_replay', replay_id=replay_id))


@routes.route('/peep/upload', methods=['POST'])
@admin_only
def upload_pick():
    """Admin peep pic upload"""

    pic = request.files['pic'] if 'pic' in request.files else None
    pic_filename = secure_filename(pic.filename) if pic is not None else None
    if not pic_filename:
        flash('No image file selected')
        return redirect(url_for('views.peep'))

    replay = request.form['replay']
    replay_id = None
    if replay:
        if '/' in replay:
            replay = replay[replay.rfind('/') + 1:]
        if replay.isdigit():
            replay_id = int(replay)
        else:
            flash('Invalid replay reference format. Enter replay ID or URL')
            return redirect(url_for('views.peep'))

    pic_id = save_pic(pic, pic_filename, replay_id)

    return redirect(url_for('views.peep', pic_id=pic_id))


@routes.route('/analytics')
@admin_only
def analytics_report():
    """View goaccess report output"""

    return send_from_directory('resource', 'analytics.html')


@routes.route('/admin')
@admin_only
def console():
    """Control panel for bans, reparse, etc"""
    replays = get_all_replays()
    savers = defaultdict(int)
    for replay in replays:
        saver_id = replay['saverPlayerId']
        savers[replay.player_names[saver_id]] += 1
    uploader_ips = get_all_uploader_ips()
    savers = sorted(savers.items(), key=lambda i: i[1], reverse=True)
    return admin_page('admin.html', 'Admin console', nav='admin', replays=replays, uploader_ips=uploader_ips, savers=savers)


@routes.route('/admin/wig.db')
@admin_only
def download_replay_db():
    """Replay database download"""

    filename = f'wig.{datetime.utcnow().replace(microsecond=0).isoformat()}.db'
    return send_file(get_db('wig.db'), attachment_filename=filename, as_attachment=True, cache_timeout=-1)


@routes.route('/admin/replaydata.zip')
@admin_only
def download_replay_data():
    """Replay data .JSON download"""

    archive_path = get_temp('replaydata.zip')
    if path.isfile(archive_path):
        remove(archive_path)

    with ZipFile(archive_path, "w", ZIP_DEFLATED) as archive:
        for data_file in glob(get_replay_data('*.json')):
            archive.write(data_file, path.basename(data_file))

    filename = f'replaydata.{datetime.utcnow().replace(microsecond=0).isoformat()}.zip'
    return send_file(archive_path, attachment_filename=filename, as_attachment=True, cache_timeout=-1)
