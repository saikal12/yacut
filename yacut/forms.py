from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp

from .constants import (LINKS_LEN_MIN, ORIGINAL_LEN_MAX, PATTERN_SHORT_URL,
                        SHORT_LEN_MAX)


class LinkForm(FlaskForm):
    original_link = URLField(
        'Введите название ссылки',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(LINKS_LEN_MIN, ORIGINAL_LEN_MAX),
                    URL(require_tld=True, message='Некорректный URL')]

    )
    custom_id = URLField(
        'Введите название короткой ссылки',
        validators=[Length(LINKS_LEN_MIN, SHORT_LEN_MAX,
                           message=f'Ссылка не должна превышать {SHORT_LEN_MAX} символов'), Optional(),
                    Regexp(PATTERN_SHORT_URL,)
                    ])
    submit = SubmitField('Добавить')
