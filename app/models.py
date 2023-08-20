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

users_paniers = db.Table('users_paniers',
    db.Column('user_id', db.ForeignKey('usersdata.id')),
    db.Column('panier_id', db.Integer,  db.ForeignKey('panier.id'))
)

class UsersData(db.Model, UserMixin):
    __tablename__='usersdata'
    id = db.Column(db.Integer, primary_key=True)
    Image = db.Column(db.String, nullable=True)
    Biographie = db.Column(db.Text, nullable=True)
    Username = db.Column(db.String, nullable=False, unique=True)
    Password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    paniers = db.relationship('Panier', secondary=users_paniers, back_populates='users')
    articles = db.relationship('Articles', backref='usersdata')

    def __repr__(self):
        return f'<Articles: {self.id}--{self.Username} >'


class Articles(db.Model):
        __tablename__ = 'articles'
        id = db.Column(db.Integer, primary_key=True, autoincrement = True)
        name = db.Column(db.String, unique=True, nullable=False)
        category = db.Column(db.String, nullable=False)
        Description = db.Column(db.String, nullable=False)
        Statut  = db.Column(db.Boolean, default=False, nullable=False)
        date_arrive = db.Column(db.Date, nullable=False)
        details = db.Column(db.Text, nullable=False)
        price = db.Column(db.Integer, nullable=False)
        quantity = db.Column(db.Integer, nullable=False)
        image = db.Column(db.String, nullable=False)
        user_id = db.Column(db.Integer, db.ForeignKey("usersdata.id"))

        def __repr__(self):
            return f'<Articles: {self.id}--{self.name} >'
        


class Panier(db.Model):
    __tablename__ = 'panier'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("usersdata.id") ,nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey("articles.id") ,nullable=False)
    quantite = db.Column(db.Integer)
    users = db.relationship('UsersData', secondary=users_paniers, back_populates='paniers')


