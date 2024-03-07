import random
import string

import choice
import secrets

from . import app, db
from .forms import LinkForm
from flask import render_template, flash, request, redirect
from .models import URLMap


def get_unique_short_id():
    lenth = 6
    res = ''.join(secrets.choice(string.digits + string.ascii_letters) for _ in range(lenth))
    return res


@app.route('/', methods=['GET', 'POST'])
def getlink():
    form = LinkForm()
    if form.validate_on_submit():
        original = form.original_link.data
        custom_id = form.custom_id.data
        if URLMap.query.filter_by(original=original).first():
            flash('такая ссылка уже есть в базе данных', )
            return render_template('yacut.html', form=form)
        if custom_id is None:
            custom_id = get_unique_short_id()
        if URLMap.query.filter_by(custom_id=custom_id).first():
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('yacut.html', form=form)
        urlmap = URLMap(
            original=original,
            custom_id=custom_id
        )
        db.session.add(urlmap)
        db.session.commit()
        flash(f'Ваша новая ссылка готова: '
              f'<a href="{request.base_url}{custom_id}">'
              f'{request.base_url}{custom_id}</a>')
    return render_template('yacut.html', form=form)


@app.route('/<string:short>', methods=['GET'])
def yacat_redirect(short):
    return redirect(
        URLMap.query.filter_by(short=short).first_or_404().original)



