import datetime
from functools import wraps

from flask import abort, flash, session, redirect, request, render_template, url_for
from werkzeug.security import generate_password_hash

from models import db, Category, User, Dish, Order
from forms import CartForm, UserForm
from app import app


@app.route('/')
def main():
    categories = db.session.query(Category).all()
    dish_list = [db.session.query(Dish).get(i) for i in session.get('cart', [])]
    amount = 0
    for dish in dish_list:
        amount += dish.price
    return render_template('main.html',
                           categories=categories,
                           amount=amount,
                           len=len(dish_list))


@app.route('/cart/')
def cart():
    is_del = False
    if session.get('delete'):
        is_del = True
        session['delete'] = False
    form = CartForm()
    dish_list = [db.session.query(Dish).get(i) for i in session.get('cart', [])]
    amount = 0
    for dish in dish_list:
        amount += dish.price
    if request.method == 'POST':
        name = form.name.data
        address = form.address.data
        email = form.user_mail.data
        phone = form.phone.data
        date = datetime.date.today().strftime("%d.%m.%Y")
        status = "Выполняется"
        order_form = Order(address=address,
                           name=name,
                           phone=phone,
                           date=date,
                           amount=amount,
                           status=status,
                           user_email=email
                           )
        for dish in dish_list:
            order_form.dishes.append(dish)
        db.session.add(order_form)
        db.session.commit()
        session['cart'] = []
        return redirect('/ordered/')
    else:
        return render_template('cart.html',
                               cart=session.get('cart', []),
                               dish_list=dish_list,
                               len=len(dish_list),
                               amount=amount,
                               is_del=is_del,
                               is_auth=session.get('is_auth', False),
                               form=form
                               )


@app.route('/account/')
def account():
    return render_template('account.html')


@app.route('/auth/')
def auth():
    return render_template('login.html')


@app.route('/register/')
def register():
    form = UserForm()
    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        email = form.mail.data
        password = form.password.data
        user = User(name=name, mail=email, password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        return redirect('/auth/')
    return render_template('login.html', form=form)


@app.route('/logout/')
def login():
    return render_template('login.html')


@app.route('/ordered/')
def order():
    return render_template('ordered.html')


@app.route('/add_to_cart/<int:dish_id>/')
def add_to_cart(dish_id):
    cart = session.get('cart', [])
    cart.append(dish_id)
    session['cart'] = cart
    return redirect(url_for('cart'))


@app.route('/delete_from_cart/<int:dish_id>/')
def delete_from_cart(dish_id):
    cart = session.get('cart', [])
    cart.remove(dish_id)
    session['cart'] = cart
    session['delete'] = True
    return redirect('/cart/')


@app.errorhandler(404)
def not_found(error):
    return "Not Found", 404
