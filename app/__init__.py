from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from .config import Config
import os



app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config.from_object(Config)
basedir = os.path.abspath(os.path.dirname(__file__))

db_info = {
    "host": "localhost",
    "user": "postgres",
    "port": "5432",
    "psw": "bayernmunich",
    "database": "ShopOnlineDB"
}
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_info['user']}:{db_info['psw']}@{db_info['host']}/{db_info['database']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'Login'
from app import routes, models



