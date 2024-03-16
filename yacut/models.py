import secrets
import string
from datetime import datetime
from re import match

from flask import url_for

from yacut import db

from .constants import (ORIGINAL_LEN_MAX, PATTERN_SHORT_URL, PATTERN_URL,
                        SHORT_LEN_MAX, YACUT_REDIRECT)


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_LEN_MAX), nullable=False)
    short = db.Column(db.String(SHORT_LEN_MAX), unique=True)
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
    def get_unique_short_id():
        lenth = 6
        res = ''.join(secrets.choice(
            string.digits + string.ascii_letters
        ) for _ in range(lenth))
        if URLMap.query.filter_by(short=res).first():
            return URLMap.get_unique_short_id()
        return res

    @staticmethod
    def validate_data(data):
        if not data.get('custom_id'):
            data['custom_id'] = URLMap.get_unique_short_id()
        elif URLMap.query.filter_by(short=data['custom_id']).first():
            raise Exception('Предложенный вариант короткой ссылки уже существует.')
        if not match(PATTERN_URL, data.get('url')):
            raise Exception('Указано недопустимое имя для ссылки')
        custom_id = data.get('custom_id')
        if custom_id and not match(PATTERN_SHORT_URL, custom_id):
            raise Exception('Указано недопустимое имя для короткой ссылки')
        return data

    @staticmethod
    def create_new_object(data):
        data = URLMap.validate_data(data)
        url_map = URLMap()
        url_map.from_dict(data)
        db.session.add(url_map)
        db.session.commit()
        return url_map

    @staticmethod
    def get_by_short_id(short):
        return URLMap.query.filter_by(short=short).first()
