from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, URLField
from wtforms.validators import DataRequired, Length, Optional


class LinkForm(FlaskForm):
    original_link = StringField(
        'Введите название ссылки',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 128)]
    )
    custom_id = StringField(
        'Введите название короткой ссылки',
        validators=[Length(1, 16, message='Ссылка не должна превышать 16 символов'), Optional()])
