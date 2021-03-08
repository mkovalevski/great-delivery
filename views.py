import datetime

from flask import session, redirect, request, render_template
from werkzeug.security import generate_password_hash

from models import db, Category, User, Dish, Order
from forms import CartForm, UserForm, AuthForm
from app import app


def make_dish_list():
    dish_list = [db.session.query(Dish).get_or_404(i) for i in session.get('cart', [])]
    amount = 0
    for dish in dish_list:
        amount += dish.price
    return dish_list, amount


def binary_search(_list, value):
    print(len(_list))
    mid = len(_list) // 2
    low = 0
    high = len(_list) - 1
    while _list[mid].id != value and low <= high:
        if value > _list[mid].id:
            low = mid + 1
        else:
            high = mid - 1
        mid = (low + high) // 2
    if low > high:
        print("No value")
        return False
    else:
        print("ID =", mid)
        return True


@app.route('/')
def main():
    categories = db.session.query(Category).all()
    dish_list, amount = make_dish_list()
    return render_template('main.html',
                           categories=categories,
                           amount=amount,
                           len=len(dish_list),
                           is_auth=session.get('is_auth', False))


@app.route('/cart/', methods=['GET', 'POST'])
def cart():
    is_del = False
    if session.get('delete'):
        is_del = True
        session['delete'] = False
    form = CartForm()
    dish_list, amount = make_dish_list()
    if request.method == 'POST':
        name = form.name.data
        address = form.address.data
        email = form.user_mail.data
        phone = form.phone.data
        date = datetime.date.today().strftime("%d.%m.%Y")
        status = "В исполнении"

        order_form = Order(address=address,
                           name=name,
                           phone=phone,
                           date=date,
                           mail=email,
                           amount=amount,
                           status=status,
                           user_id=session['user_id']
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
    dish_list, amount = make_dish_list()
    if session['is_auth']:
        user = db.session.query(User).get_or_404(session['user_id'])
        orders = user.orders
        return render_template('account.html',
                               orders=orders,
                               db=db,
                               Dish=Dish,
                               amount=amount,
                               len=len(dish_list),
                               is_auth=session.get('is_auth', False))
    return redirect('/auth/')


@app.route('/auth/', methods=['GET', 'POST'])
def auth():
    dish_list, amount = make_dish_list()
    if session.get('user_id'):
        return redirect('/account/')
    else:
        form = AuthForm()
        if request.method == 'POST':
            user = db.session.query(User).filter(User.mail == form.mail.data).first()
            if user and user.password_valid(form.password.data):
                session['user_id'] = user.id
                session['is_auth'] = True
                return redirect('/account/')
            else:
                err = 'Неверный e-mail или пароль'
                return render_template('auth.html',
                                       form=form,
                                       amount=amount,
                                       len=len(dish_list),
                                       error_msg=err)
        return render_template("auth.html",
                               form=form,
                               len=len(dish_list),
                               amount=amount)


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = UserForm()
    dish_list, amount = make_dish_list()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.mail.data
        password = form.password.data
        user_exists = User.query.filter_by(mail=email).first()
        if user_exists:
            error_msg = 'Пользователь существует'
            return render_template("register.html",
                                   form=form,
                                   amount=amount,
                                   len=len(dish_list),
                                   error_msg=error_msg)
        user = User(mail=email, password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        return redirect('/auth/')
    return render_template('register.html',
                           form=form,
                           amount=amount,
                           len=len(dish_list))


@app.route('/logout/')
def login():
    if session.get('user_id'):
        session.pop('user_id')
        session['is_auth'] = False
    return redirect('/auth/')


@app.route('/ordered/')
def order():
    return render_template('ordered.html')


@app.route('/add_to_cart/<int:dish_id>/')
def add_to_cart(dish_id):
    dishes = db.session.query(Dish).all()
    print("Длина", len(dishes))
    if binary_search(dishes, dish_id):
        cart = session.get('cart', [])
    else:
        return "Not Found", 404
    cart.append(dish_id)
    session['cart'] = cart
    return redirect('/')


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
