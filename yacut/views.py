from flask import flash, redirect, render_template

from . import app
from .error_handlers import InvalidUsage
from .forms import LinkForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = LinkForm()
    if form.validate_on_submit():
        data = {
            'url': form.original_link.data,
            'custom_id': form.custom_id.data
        }
        try:
            url_map = URLMap.create_new_object(data)
        except InvalidUsage as e:
            flash(e.message)
        else:
            return render_template('index.html', form=form, short_url=url_map.short)
    return render_template('index.html', form=form)


@app.route('/<string:short>', methods=['GET'])
def yacut_redirect(short):
    long_link = URLMap.get_short_id(short)
    if not long_link:
        raise InvalidUsage('Указанный id не найден', 404)
    return redirect(long_link.original)
