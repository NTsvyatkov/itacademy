from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
mysql_config='mysql+mysqldb://root:111@localhost/store_DB'
engine = create_engine(mysql_config)
Base = declarative_base()
Session = sessionmaker(bind=engine)
db_session = Session()
