"""
Routes and views for the flask application.
"""

import random
from flask import url_for
from perchweb import app
from perchweb.handler import standard_page


@app.route('/')
def index():
    """Index"""
    return standard_page('index.html', 'Replays', nav='index')


@app.route('/highperching')
def guide():
    """The art"""
    return standard_page('guide.html', 'The Art of Highperching', nav='guide')


# Todo: Store number of files, allow admin uploads etc
random.seed()
pic_max = 89
@app.route('/peep/', defaults={'pic_id': None})
@app.route('/peep/<int:pic_id>')
def peep(pic_id):
    """Sometimes random pictures"""
    pic_id = random.randint(1, pic_max) if pic_id is None else pic_id
    return standard_page('peep.html', 'Peep a pic', nav='peep',
                         pic_url=f'/static/images/peep/{pic_id}.jpg',
                         perma=url_for('peep', pic_id=pic_id))
