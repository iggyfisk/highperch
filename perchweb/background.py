"""
BG styles, set by cookie. Dependent on 'Background switching' sections in CSS and JS,
as well as the listing in layout.html
"""

from flask import request

cookie_name = 'HP_bg'
styles = [
    {'style': 'lordaeron', 'name': 'Lordaeron', 'icon': 'lordico.png'},
    {'style': 'barrens', 'name': 'Barrens', 'icon': 'barrensico.png'},
    {'style': 'icecrown', 'name': 'Icecrown', 'icon': 'iceico.png'},
    {'style': 'lwinter', 'name': 'Lordaeron Winter', 'icon': 'lordwico.png'},
]
style_keys = {s['style'] for s in styles}

def add_background():
    active_style = styles[0]['style']
    cookie_style = request.cookies[cookie_name] if cookie_name in request.cookies else None
    if cookie_style in style_keys:
        active_style = cookie_style

    return {'background_style': active_style, 'backgrounds': styles}
