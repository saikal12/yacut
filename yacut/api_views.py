

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def get_link():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    url_map = URLMap.create_new_object(data)
    return jsonify(url_map.to_dict()), 201


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_original_link(short):
    redirect = URLMap.get_short_id(short)
    if not redirect:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': redirect.original}), 200
