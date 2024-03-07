from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def get_link():
    data = request.get_json()
    if 'url' not in data:
        raise InvalidAPIUsage('В запросе отсутствуют обязательные поля')
    if data.custom_id is None:
        data['custom_id'] = get_unique_short_id()
    if URLMap.query.filter_by(short=data.custom_id).first():
        raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.')
    urlmap = URLMap()
    urlmap.from_dict(data)
    db.session.add(urlmap)
    db.session.commit()
    return jsonify({'urlmap': urlmap.to_dict()}), 201


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_link(short_id):
    redirect = URLMap.query.filter_by(short=short_id).first().original
    if not redirect:
        raise InvalidAPIUsage('Указанный id ссылки  не найден')
    return jsonify({'url': redirect})




