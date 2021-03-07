from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, DataRequired, EqualTo


class CartForm(FlaskForm):
    name = StringField('name', [InputRequired(message='Введите имя'),
                                Length(min=2, message='Имя должно содержать минимум 2 символа')])
    address = StringField('address', [InputRequired(message='Введите адрес')])
    user_mail = StringField('mail', [Email(message='Неверные данные')])
    phone = StringField('phone', [Length(min=7, message='Неверный телефон')])


class UserForm(FlaskForm):
    name = StringField('name', [InputRequired(message='Введите имя'),
                                Length(min=2, message='Поле должно содержать минимум два символа')])
    mail = StringField('mail', [Email(message='Неверные данные')])
    password = PasswordField('password', validators=[
                            InputRequired(message='Введите пароль'),
                            Length(min=5, message='Пароль должен быть не менее 5 символов'),
                            EqualTo('confirm_password', message="Пароли не одинаковые")]
                            )
    confirm_password = PasswordField('confirm_password', InputRequired(message='Повторите пароль'))