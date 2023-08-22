from app import db 
from sqlalchemy import Column, Integer, ForeignKey, String, Date, Text, Boolean, DateTime
from flask_login import UserMixin
from datetime import datetime


class ImageDefilante(db.Model):
    __tablename__ = 'imagedefilante'
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String, nullable=False)
    details = db.Column(db.String, nullable=False)

    
    def __repr__(self):
        return f'<Articles: {self.id}--{self.image} >'  
class UsersData(db.Model, UserMixin):
    __tablename__ = 'usersdata'
    id = db.Column(db.Integer, primary_key=True)
    Image = db.Column(db.String, nullable=True)
    Biographie = db.Column(db.Text, nullable=True)
    Username = db.Column(db.String, nullable=False, unique=True)
    Password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    panier = db.relationship('Panier', backref='usersdata', uselist=False)
    articles = db.relationship('Articles', backref='usersdata')
    
    def __repr__(self):
        return f'<UsersData: {self.id}--{self.Username}>'
    


association_table_articles_panier = db.Table('association',
    db.Column('article_id', db.Integer, db.ForeignKey('articles.id')),
    db.Column('panier_id', db.Integer, db.ForeignKey('panier.id'))
)



class Articles(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    Description = db.Column(db.String, nullable=False)
    date_arrive = db.Column(db.Date, nullable=False)
    details = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('usersdata.id'))
    
    def __repr__(self):
        return f'<Articles: {self.id}--{self.name}>'


class Panier(db.Model):
    __tablename__ = 'panier'
    id = db.Column(db.Integer, primary_key=True)
    quantite = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('usersdata.id'))
    articles_paniers = db.relationship('Articles',secondary=association_table_articles_panier, backref='')

