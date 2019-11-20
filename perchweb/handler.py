"""
Sets up a request pipeline with shared page processing (backgrounds, footer quotes etc)
There's probably a standard way to do this, but homerolling until I discover it
"""

from datetime import datetime
from flask import render_template
from perchweb.background import add_background

def standard_page(template, title, **attributes):
    bg_attributes = add_background()

    return render_template(
        template,
        title=title,
        year=datetime.now().year,
        **bg_attributes,
        **attributes,
    )
