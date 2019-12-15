"""
Sets up a request pipeline with shared page processing (backgrounds, footer quotes etc)
There's probably a standard way to do this, but homerolling until I discover it
"""

from datetime import datetime
from flask import render_template, abort
from background import add_background
from chatlog import add_chatlog
from auth import add_auth_attributes
from templatefilters import lighten_color

def standard_page(template, title, **attributes):
    auth_attributes = add_auth_attributes()
    bg_attributes = add_background()
    chat_attributes = add_chatlog()

    return render_template(
        template,
        title=title,
        year=datetime.now().year,
        lighten_color=lighten_color,
        **auth_attributes,
        **chat_attributes,
        **bg_attributes,
        **attributes,
    )


def admin_page(template, title, **attributes):
    """ Just in case someone forgets to add a decorator """
    auth_attributes = add_auth_attributes()
    if not auth_attributes['is_admin']:
        abort(403)

    bg_attributes = add_background()
    chat_attributes = add_chatlog()

    return render_template(
        template,
        title=title,
        year=datetime.now().year,
        **auth_attributes,
        **chat_attributes,
        **bg_attributes,
        **attributes,
    )
