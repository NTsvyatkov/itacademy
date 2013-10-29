from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
db_engine = create_engine("sqlite:///data.db", echo=True)


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from models.product_dao import Product, Dimension

