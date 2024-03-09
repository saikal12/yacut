import secrets
import string

from flask import flash, redirect, render_template

from yacut.error_handlers import InvalidAPIUsage

from . import app
from .forms import LinkForm
from .models import URLMap


def get_unique_short_id():
    lenth = 6
    res = ''.join(secrets.choice(string.digits + string.ascii_letters) for _ in range(lenth))
    return res


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = LinkForm()
    if form.validate_on_submit():
        try:
            url_map = URLMap.create_new_object(form)
            return render_template('index.html', short_url=url_map.short)
        except InvalidAPIUsage as e:
            flash(str(e))
    return render_template('index.html', form=form)


@app.route('/<string:short>', methods=['GET'])
def yacut_redirect(short):
    long_link = URLMap.get_from_db(short, short)
    return redirect(long_link.original)
