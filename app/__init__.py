from flask import Flask , Blueprint
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
# blueprint = Blueprint(app)

app.config.from_object(Config)
basedir = os.path.abspath(os.path.dirname(__file__))

db_info = {
    "host": "localhost",
    "user": "postgres",
    "port": "5432",
    "psw": "bayernmunich",
    "database": " shoponlinedb_hgq9" 
}


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")

# postgres://shoponlinedb_b80p_user:y2YaQzxhXcRM0MT6I33Luvzy50SPX3vb@dpg-cm2p2ti1hbls73frfmd0-a.frankfurt-postgres.render.com/shoponlinedb_b80p

# app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_info['user']}:{db_info['psw']}@{db_info['host']}/{db_info['database']}"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# postgres://lucas09009:d149F3a5naH02rVcXXKH3Ge2qLQC3w1Z@dpg-cm2o44a1hbls73fr0r00-a.frankfurt-postgres.render.com/shoponlinedb_hgq9
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True
# app.config['MAIL_USERNAME'] = 'awetandtesfit@gmail.com'
# app.config['MAIL_PASSWORD'] = 'Micheal79'


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