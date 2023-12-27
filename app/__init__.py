from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from .config import Config
from flask_bootstrap import Bootstrap
from flask_mail import Message, Mail
import os
import stripe



app = Flask(__name__)
bcrypt = Bcrypt(app)
bootstrap = Bootstrap(app)

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
# postgres://shoponlinedb:XfIGBJfvYyDAEOtgzYbhQW9tuSawOUMK@dpg-cm2vf321hbls73fu5lf0-a.frankfurt-postgres.render.com/shoponlinedb_jof6
# app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_info['user']}:{db_info['psw']}@{db_info['host']}/{db_info['database']}"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# print('sdsdsdsdsd',app.config['SQLALCHEMY_DATABASE_URI'])

app.config['MAIL_SERVER'] = 'smtp.mailtrap.io'
app.config['MAIL_PORT'] = 587 
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'api'
app.config['MAIL_PASSWORD'] = '45a1f9d819f20b682bf406b368f6e5c8'


db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'Login'
mail = Mail(app)


stripe.api_key = os.getenv("STRIPE_API_KEY")
from app import routes, models




class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f'event type: {event.event_type}  path : {event.src_path}')

event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, path='.', recursive=False)
observer.start()