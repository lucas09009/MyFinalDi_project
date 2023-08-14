from app import db 
from sqlalchemy import Column, Integer, ForeignKey, String, Date, Text, Boolean
from flask_login import UserMixin


class ImageDefilante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String, nullable=False)
    details = db.Column(db.String, nullable=False)

class UsersData(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String, nullable=False, unique=True)
    Password = db.Column(db.String, nullable=False, unique=True)
    is_admin = db.Column(db.Boolean, default=False)

class Articles(db.Model):
        __tablename__ = 'Articles'
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
        # users_id = db.Column(db.Integer, db.ForeignKey('users_data.id'),nullable=True)

        def __repr__(self):
            return f'<Articles: {self.id}--{self.name} >'