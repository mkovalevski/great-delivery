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
    mail = StringField('mail', [InputRequired(message='Введите e-mail'), Email(message='Неверно введен e-mail')])
    password = PasswordField('password', validators=[
                            DataRequired(),
                            Length(min=5, message='Пароль должен быть не менее 5 символов'),
                            EqualTo('confirm_password', message="Пароли не одинаковые")]
                            )
    confirm_password = PasswordField('confirm_password', [InputRequired(message='Повторите пароль')])


class AuthForm(FlaskForm):
    mail = StringField('mail', [InputRequired(message='Введите e-mail'), Email(message='Неверно введен e-mail')])
    password = PasswordField('password', )
