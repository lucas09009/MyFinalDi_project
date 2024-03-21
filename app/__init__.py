from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from .config import Config
import os, stripe
from flask_mail import Mail
from dotenv import load_dotenv


app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config.from_object(Config)
basedir = os.path.abspath(os.path.dirname(__file__))
db_info = {
    "host": "dpg-cm3g5fen7f5s73boed70-a.frankfurt-postgres.render.com",
    "user": "shoponlinedb",
    "port": "5432",
    "psw": "Ts1RtwjNdFoSpl5oFO2Qw65wb7heFEnW",
    "database": "shoponlinedb_ksv8" 
}

# postgres://shoponlinedb:Ts1RtwjNdFoSpl5oFO2Qw65wb7heFEnW@dpg-cm3g5fen7f5s73boed70-a.frankfurt-postgres.render.com/shoponlinedb_ksv8

# db_info = {
#     "host": "localhost",
#     "user": "postgres",
#     "port": "5432",
#     "psw": "bayernmunich",
#     "database": "ShopOnlineDB" 
# }

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_info['user']}:{db_info['psw']}@{db_info['host']}/{db_info['database']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False




app.config['STRIPE_PUBLIC_KEY'] ='pk_test_51Nn1NTI0GTnWYq6mdWdyNj22RpBUNdvf5MX2LnvjHiil7kJgEKhyKcGjNPv9J5yUJtC0apOLGAbQWMqVKfjVdqsB00oEJwGiNS'
app.config['STRIPE_SECRET_KEY'] ='sk_test_51Nn1NTI0GTnWYq6mQaKiiw0LLjXCRrkKpDxTmtigyqWWPrBt16n7qzPlyg8qLuCZfgND42UF1jn3BS9VXv4TCxsr00k5GoTpbJ'

stripe.api_key = app.config['STRIPE_SECRET_KEY'] 


app.config['MAIL_SERVER'] ='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = 'luckpegan@gmail.com'
app.config['MAIL_PASSWORD'] = "tuli jmxk efeo oduz "
app.config['MAIL_DEFAULT_SENDER'] =('Mongo Market', 'luckpvghegan@gmail.com')
app.config['MAIL_MAX_EMAILS'] = None
app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_ASCII_ATTACHMENTS' ]= False

#Initialisation de SQLAlchemy
db = SQLAlchemy(app) 

#Initialisation de Migrate
migrate = Migrate(app, db)

#Création d'une instance de LoginManager() et initialisation
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'Login' 


load_dotenv()  
mail = Mail(app)
from app import routes, models
