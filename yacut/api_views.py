from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage, ValidationError
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def get_link():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    try:
        url_map = URLMap.create_new_object(data)
    except ValidationError as e:
        raise InvalidAPIUsage(str(e))
    else:
        return jsonify(url_map.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_original_link(short):
    redirect = URLMap.get_by_short_id(short)
    if not redirect:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': redirect.original}), HTTPStatus.OK
