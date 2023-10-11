from .models import Articles, Category, Promotions
from app import app, db


def ChoixDeCategories():
    articles_list = []
    with app.app_context():
        for c in Category.query.all():
            data = (c.id,c.name)
            articles_list.append(data)
    return articles_list 


def get_categories_with_icons():
    categories = Category.query.all()
    categories_with_icons = {category.name: category.icon_name for category in categories}
    return categories_with_icons


def choixDePromo():
    liste = []
    data = Promotions.query.all()
    for items in data:
        liste.append(items)
    return liste
