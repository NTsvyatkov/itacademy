from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+mysqldb://root:111@localhost/store_DB')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()



