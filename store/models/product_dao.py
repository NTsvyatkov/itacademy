from models import Base, session
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
    def add_product(name, description, price, dimension):
        p = Product(name, description, price, session.query(Dimension).filter_by(name=dimension).first())
        session.add(p)
        session.commit()

    @staticmethod
    def search_product(name):
        return session.query(Product).filter_by(name=name).all()

    @staticmethod
    def get_product(id):
        return session.query(Product).get(id)

    @staticmethod
    def upd_product(id, new_name, new_description, new_price, new_dimension):
        entry = Product.get_product(id)
        entry.name = new_name
        entry.description = new_description
        entry.price = new_price
        entry.dimension = session.query(Dimension).filter_by(name=new_dimension).first()
        session.commit() 


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
        return session.query(Dimension).get(id)

    @staticmethod
    def add_dimension(name):
        d = Dimension(name)
        session.add(d)
        session.commit()

    @staticmethod
    def update_dimension(id, new_name,):
        entry = session.query(Dimension).get(id)
        entry.name = new_name
        session.commit()
