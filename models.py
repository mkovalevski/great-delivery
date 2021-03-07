from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

orders_dishes_association = db.Table('orders_dishes',
                                     db.Column('dish_id', db.Integer, db.ForeignKey('dishes.id')),
                                     db.Column('order_id', db.Integer, db.ForeignKey('orders.id'))
                                     )


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    mail = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)

    orders = db.relationship('Order', back_populates='user')

    @property
    def password(self):
        # Запретим прямое обращение к паролю
        raise AttributeError("Вам не нужно знать пароль!")

    @password.setter
    def password(self, password):
        # Устанавливаем пароль через этот метод
        self.password_hash = generate_password_hash(password)

    def password_valid(self, password):
        # Проверяем пароль через этот метод
        # Функция check_password_hash превращает password в хеш и сравнивает с хранимым
        return check_password_hash(self.password_hash, password)


class Dish(db.Model):
    __tablename__ = 'dishes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=False)
    picture = db.Column(db.String)

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Category', back_populates='dishes')
    orders = db.relationship('Order', secondary=orders_dishes_association, back_populates='dishes')


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)

    dishes = db.relationship('Dish', back_populates='category')


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    date = db.Column(db.String)
    amount = db.Column(db.Integer)
    status = db.Column(db.String)
    mail = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    address = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='orders')
    dishes = db.relationship('Dish', secondary=orders_dishes_association, back_populates='orders')
