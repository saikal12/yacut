from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

PATTERN_SHORT_URL = r'^[A-Za-z0-9_]+$'


class LinkForm(FlaskForm):
    original_link = URLField(
        'Введите название ссылки',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 128)]
    )
    custom_id = URLField(
        'Введите название короткой ссылки',
        validators=[Length(1, 16, message='Ссылка не должна превышать 16 символов'), Optional(),
                    Regexp(PATTERN_SHORT_URL,)
                    ])
    submit = SubmitField('Добавить')
