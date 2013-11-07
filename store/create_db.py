__author__ = 'alex'
from sqlalchemy import create_engine
mysql_config='mysql+mysqldb://root:111@localhost/'
engine = create_engine(mysql_config)
engine.execute("CREATE DATABASE IF NOT EXISTS store_DB ")
engine.execute("USE store_DB")
from models.product_dao import Product
from models.user_dao import UserDao
from models.order_dao import Order
from models import Base
print Base.metadata
Base.metadata.create_all(engine)