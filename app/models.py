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
    __tablename__='usersdata'
    id = db.Column(db.Integer, primary_key=True)
    Image = db.Column(db.String, nullable=True)
    Biographie = db.Column(db.Text, nullable=True)
    Username = db.Column(db.String, nullable=False, unique=True)
    Password = db.Column(db.String, nullable=False, unique=True)
    is_admin = db.Column(db.Boolean, default=False)
    # paniers = db.relationship('Panier', secondary=user_panier_associations, back_populates='users')
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
        user_id = db.Column(db.Integer, db.ForeignKey("usersdata.id"),nullable=True)
        # users_cart_items = db.relationship('Articles', back_populates='cart_items')

        def __repr__(self):
            return f'<Articles: {self.id}--{self.name} >'
        

# user_panier_association = db.Table(
#     'user_panier_association',
#     db.Column('user_id', db.Integer, db.ForeignKey('usersdata.id')),
#     db.Column('panier_id', db.Integer, db.ForeignKey('panier.id'))
# )


# class Panier(db.Model):
#     __tablename__ = 'panier'
#     id = db.Column(db.Integer, primary_key=True)
#     image = db.Column(db.String, nullable=False)
#     users = db.relationship('UsersData', secondary=user_panier_association, back_populates='paniers')


# user_panier_association = db.Table(
#     'user_panier_association',
#     db.Column('user_id', db.Integer, db.ForeignKey('usersdata.id')),
#     db.Column('panier_id', db.Integer, db.ForeignKey('panier.id'))
# )
