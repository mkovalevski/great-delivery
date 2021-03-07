from flask import Flask
from flask_migrate import Migrate
from flask_wtf import CSRFProtect

from config import Config
from models import db, User, Dish, Category, Order

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
csrf = CSRFProtect(app)

migrate = Migrate(app, db)


from views import *

if __name__ == "__main__":
    app.run()
