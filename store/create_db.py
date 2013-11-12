from sqlalchemy import create_engine
from models.product_dao import Product
from models.user_dao import UserDao
from models.order_dao import Order
from models import Base


mysql_config='mysql+mysqldb://root:111@localhost/'
engine = create_engine(mysql_config)
engine.execute("CREATE DATABASE store_DB ")
engine.execute("USE store_DB")

print Base.metadata
Base.metadata.create_all(engine)