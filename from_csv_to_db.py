import csv

from app import app
from models import db, Category, Dish

with app.app_context():
    with open('delivery_categories.csv', newline='', encoding='utf-8') as csv_file:
        spam_reader = csv.reader(csv_file, delimiter=' ', quotechar='|')
        data = []
        for row in spam_reader:
            data.append(row)
        for cat in data[1:]:
            db.session.add(Category(title=cat[0][2:]))
        db.session.commit()
    with open('delivery_items.csv', encoding='utf-8') as csv_file:
        delivery_items = csv.DictReader(csv_file)
        for delivery_item in delivery_items:
            db.session.add(Dish(**delivery_item))
    db.session.commit()
