from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session,sessionmaker
# from flask_sqlalchemy import SQLAlchemy
# from passlib.hash import sha256_crypt


app= Flask(__name__)
app.config['SECRET_KEY']="thisisasecret"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'

db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)

from app import routes