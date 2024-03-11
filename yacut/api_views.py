from re import match

from flask import jsonify, request, flash

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .constants import PATTERN_SHORT_URL, PATTERN_URL


@app.route('/api/id/', methods=['POST'])
def get_link():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    if not match(PATTERN_URL, data.get('url')):
        raise InvalidAPIUsage('Указано недопустимое имя для ссылки')
    custom_id = data.get('custom_id')
    if custom_id and not match(PATTERN_SHORT_URL, custom_id):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    try:
        url_map = URLMap.create_new_object(data)
    except InvalidAPIUsage as e:
        raise e

    else:
        return jsonify(url_map.to_dict()), 201


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_original_link(short):
    try:
        redirect = URLMap.get_from_db(short)
    except InvalidAPIUsage as e:
        raise e
    else:
        return jsonify({'url': redirect.original}), 200
