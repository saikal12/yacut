from datetime import datetime

from flask import url_for

from yacut import db
from .error_handlers import InvalidAPIUsage
from .views import get_unique_short_id
from .constants import YACUT_REDIRECT


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(128), nullable=False)
    short = db.Column(db.String(16), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                YACUT_REDIRECT, short=self.short, _external=True
            ))

    def from_dict(self, data):
        setattr(self, 'original', data['url'])
        setattr(self, 'short', data['custom_id'])

    @staticmethod
    def create_new_object(data):
        if not data.get('custom_id'):
            data['custom_id'] = get_unique_short_id()
        if URLMap.query.filter_by(short=data['custom_id']).first():
            raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.')
        url_map = URLMap()
        url_map.from_dict(data)
        db.session.add(url_map)
        db.session.commit()
        return url_map

    @staticmethod
    def get_from_db(field_name, field_value):
        redirect = URLMap.query.filter(getattr(URLMap, field_name) == field_value).first()
        if not redirect:
            raise InvalidAPIUsage('Указанный id не найден', 404)
        return redirect