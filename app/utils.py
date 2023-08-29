from .models import Articles, Category
from app import app, db


def ChoixDeCategories():
    articles_list = []
    with app.app_context():
        for c in Category.query.all():
            data = (c.id,c.name)
            print(data)
            articles_list.append(data)
    return articles_list 


def get_categories_with_icons():
    categories = Category.query.all()
    categories_with_icons = {category.name: category.icon_name for category in categories}
    return categories_with_icons
