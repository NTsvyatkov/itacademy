from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker

#engine = create_engine('sqlite:///', echo=True)
engine = create_engine('mysql+mysqldb://root:111@localhost/pythonDB')
engine.execute("CREATE DATABASE IF NOT EXISTS  PROJECT1 ")
engine.execute("USE PROJECT1")

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)
