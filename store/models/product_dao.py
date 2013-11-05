from models import Base, db_session
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Float
from sqlalchemy.orm import relationship, backref


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    description = Column(Text)
    price = Column(Float)

    dimension_id = Column(Integer, ForeignKey('dimensions.id'))
    dimension = relationship('Dimension', backref=backref('products', lazy='dynamic'))

    def __init__(self, name, description, price, dimension):
        self.name = name
        self.description = description
        self.price = price
        self.dimension = dimension

    def __str__(self):
        return '%s, %s, %s, %s' % (self.name, self.description, self.price, self.dimension)

    @staticmethod
    def add_product(name, description, price, id):
        p = Product(name, description, price, db_session.query(Dimension).get(id))
        db_session.add(p)
        db_session.commit()

    @staticmethod
    def del_product(id):
        entry = Product.get_product(id)
        db_session.delete(entry)
        db_session.commit()

    @staticmethod
    def search_product(name):
        return db_session.query(Product).filter_by(name=name).all()

    @staticmethod
    def get_product(id):
        return db_session.query(Product).get(id)

    @staticmethod
    def upd_product(id, new_name, new_description, new_price, new_dimension):
        entry = Product.get_product(id)
        entry.name = new_name
        entry.description = new_description
        entry.price = new_price
        entry.dimension = db_session.query(Dimension).get(new_dimension)
        db_session.commit()

    @staticmethod
    def get_all_products():
        return db_session.query(Product).all()


class Dimension(Base):
    __tablename__ = 'dimensions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(10))
    
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    @staticmethod
    def get_dimension(id):
        return db_session.query(Dimension).get(id)

    @staticmethod
    def add_dimension(name):
        d = Dimension(name)
        db_session.add(d)
        db_session.commit()

    @staticmethod
    def update_dimension(id, new_name,):
        entry = db_session.query(Dimension).get(id)
        entry.name = new_name
        db_session.commit()

    @staticmethod
    def get_all_dimensions():
        return db_session.query(Dimension).all()

#Dimension.add_dimension("item")
#Dimension.add_dimension("box")
#Dimension.add_dimension("package")
#print Dimension.get_dimension(1)
#print Dimension.get_dimension(2)
#print Dimension.get_dimension(3)
