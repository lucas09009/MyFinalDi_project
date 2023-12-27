from app import db 
from sqlalchemy import Column, Integer, ForeignKey, String, Date, Text, Boolean, DateTime
from flask_login import UserMixin
from datetime import datetime


class Promotions(db.Model):
    __tablename__ = 'promotions'
    id = db.Column(db.Integer, primary_key=True)
    nom_de_la_promotion = db.Column(db.String, nullable=False)
    duree_de_la_promo = db.Column(db.Integer, nullable=False)
    reduction = db.Column(db.Integer, nullable=False)
    details = db.Column(db.Text, nullable=True)
    image = db.Column(db.String, nullable=True)
    promotions = db.relationship('Articles', backref='articles_promo', lazy=True)
    
    def __repr__(self):
        return f'<Articles: {self.id}-->' 


# class categoryPromo(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     promo_name = db.Column(db.String, nullable=False)
#     duree_de_la_promo = db.Column(db.Integer, nullable=False)
#     reduction = db.Column(db.Integer, nullable=False)
#     articles = db.relationship('Articles', backref='category', lazy=True)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    icon_name = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    articles = db.relationship('Articles', backref='category', lazy=True)




class Payement(db.Model):
    __tablename__ = 'payement'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    prix_total = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('usersdata.id'))







association_table_articles_panier = db.Table('association',
    db.Column('article_id', db.Integer, db.ForeignKey('articles.id')),
    db.Column('panier_id', db.Integer, db.ForeignKey('panier.id'))
)


class Panier(db.Model):
    __tablename__ = 'panier'
    id = db.Column(db.Integer, primary_key=True)
    quantite = db.Column(db.Integer, nullable=False)    
    user_id = db.Column(db.Integer, db.ForeignKey('usersdata.id'))
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    # articles_paniers = db.relationship('Articles',secondary=association_table_articles_panier, backref='articles')




class Commentaires(db.Model):
    __tablename__ = 'commentaires'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    commentaires = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usersdata.id'))
    user_name = db.Column(db.String)
    image = db.Column(db.String)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))

    


class ArticlesFavoris(db.Model):
    __tablename__ = 'articlesfavoris'
    id = db.Column(db.Integer, primary_key=True)
    id_of_user = db.Column(db.Integer, db.ForeignKey('usersdata.id'))
    id_of_article  = db.Column(db.Integer, db.ForeignKey('articles.id'))
    category_id  = db.Column(db.Integer)
    Username = db.Column(db.Integer)




class UsersData(db.Model, UserMixin):
    __tablename__ = 'usersdata'
    id = db.Column(db.Integer, primary_key=True)
    Image = db.Column(db.String, nullable=True)
    Biographie = db.Column(db.String(80), nullable=True)
    Username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, unique=True)
    Password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    carts = db.relationship('Panier', backref='usersdata', lazy=True)
    commentaires = db.relationship('Commentaires', backref='usersdata')
    articles_favoris = db.relationship('ArticlesFavoris', backref='usersdata')
    def __repr__(self):
        return f'<UsersData: {self.id}--{self.Username}>'
    

class Articles(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(22), nullable=False)
    Description = db.Column(db.String(30), nullable=False)
    date_arrive = db.Column(db.Date, nullable=False)
    details = db.Column(db.String(180), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    user_name = db.Column(db.String)
    user_image = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    promotion_id = db.Column(db.Integer, db.ForeignKey('promotions.id'), nullable=True)
    carts = db.relationship('Panier', backref='articles', lazy=True)
    nombre_de_vues = db.Column(db.Integer, default=0)
    commentaires = db.relationship('Commentaires', backref='articles')
    # articles_favoris = db.relationship('Articles', backref='articles')
    articles_favoris = db.relationship('ArticlesFavoris', primaryjoin="Articles.id == ArticlesFavoris.id_of_article", backref='articles', lazy=True)

    def __repr__(self):
        return f'<Articles: {self.id}--{self.name}>'


class UsersAyantVueLarticle(db.Model):
    __tablename__ = 'UserViewArticles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_of_viewer = db.Column(db.String(20), nullable=False)
























