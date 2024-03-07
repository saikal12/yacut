import secrets
import string

from flask import flash, redirect, render_template, request

from . import app, db
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
        custom_id = form.custom_id.data
        if not custom_id:
            custom_id = get_unique_short_id()
        if URLMap.query.filter_by(short=custom_id).first():
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('index.html', form=form)
        url_map = URLMap(
            original=form.original_link.data,
            short=custom_id
        )
        db.session.add(url_map)
        db.session.commit()
        flash(f'Ваша новая ссылка готова: '
              f'<a href="{request.base_url}{custom_id}">'
              f'{request.base_url}{custom_id}</a>')
    return render_template('index.html', form=form)


@app.route('/<string:short>', methods=['GET'])
def yacut_redirect(short):
    return redirect(
        URLMap.query.filter_by(short=short).first_or_404().original)
