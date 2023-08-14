import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    UPLOAD_PATH = os.getenv('UPLOAD_PATH')
    SESSION_PERMANENT = os.getenv('SESSION_PERMANENT')
    SESSION_TYPE = os.getenv('SESSION_TYPE')