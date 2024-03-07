from re import match

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id

PATTERN_SHORT_URL = r'^[A-Za-z0-9_]{1,16}$'


@app.route('/api/id/', methods=['POST'])
def get_link():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage("\"url\" является обязательным полем!")
    if not data.get('custom_id'):
        data['custom_id'] = get_unique_short_id()
    if URLMap.query.filter_by(short=data['custom_id']).first():
        raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.')
    if not match(PATTERN_SHORT_URL, data['custom_id']):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    url_map = URLMap()
    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), 201


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_original_link(short):
    redirect = URLMap.query.filter_by(short=short).first()
    if redirect is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': redirect.original}), 200
