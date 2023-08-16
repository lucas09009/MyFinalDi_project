from .models import Articles
from app import app, db


def ChoixDeCategories():
    articles_list = []
    with app.app_context():
        # db.create_all()
        for c in Articles.query.all():
            data = (c.id, c.name)
            articles_list.append(data)
    return articles_list 

