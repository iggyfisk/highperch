"""
Sets up a request pipeline with shared page processing (backgrounds, footer quotes etc)
There's probably a standard way to do this, but homerolling until I discover it
"""

from datetime import datetime
from flask import render_template, request
from background import add_background
from chatlog import add_chatlog
from admin import check_if_admin


def standard_page(template, title, **attributes):
    bg_attributes = add_background()
    chat_attributes = add_chatlog()

    return render_template(
        template,
        title=title,
        year=datetime.now().year,
        is_admin=check_if_admin(request.cookies),
        **chat_attributes,
        **bg_attributes,
        **attributes,
    )
