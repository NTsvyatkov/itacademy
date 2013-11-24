from models import Base, db_session
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Float, Boolean,and_,or_
from sqlalchemy.orm import relationship, backref


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    description = Column(Text)
    price = Column(Float)
    dimension_id = Column(Integer, ForeignKey('dimensions.id'))
    dimension = relationship('Dimension', backref=backref('products', lazy='dynamic'))
    is_deleted = Column(Boolean, default=False)

    def __init__(self, name, description, price, dimension, is_deleted=False):
        super(Product, self).__init__()
        self.name = name
        self.description = description
        self.price = price
        self.dimension = dimension
        self.is_deleted = is_deleted

    def __str__(self):
        return '%s, %s, %s, %s, %s' % (self.name, self.description, self.price, self.dimension, self.is_deleted)

    @staticmethod
    def add_product(name, description, price, id):
        p = Product(name, description, price, Dimension.query.get(id))
        db_session.add(p)
        db_session.commit()

    @staticmethod
    def del_product(id):
        entry = Product.get_product(id)
        entry.is_deleted = True
        db_session.commit()

    @staticmethod
    def search_product(name):
        return Product.query.filter_by(name=name).all()

    @staticmethod
    def get_product(id):
        return Product.query.get(id)

    @staticmethod
    def upd_product(id, new_name, new_description, new_price, new_dimension):
        entry = Product.get_product(id)
        entry.name = new_name
        entry.description = new_description
        entry.price = new_price
        entry.dimension = Dimension.query.get(new_dimension)
        db_session.commit()

    @staticmethod
    def get_all_products():
        return Product.query.filter_by(is_deleted=False).all()

    @staticmethod
    def pager_by_filter(name=None, start_price=None, end_price=None, page=None, records_per_page=None):
        query = Product.query.filter_by(is_deleted=False)
        if name:
            query = query.filter(or_(Product.name == name, Product.description == name))
        if start_price:
            query = query.filter(Product.price >= start_price)
        if end_price:
            query = query.filter(Product.price <= end_price)
        stop = page * records_per_page
        start = stop - records_per_page
        return query.filter_by(is_deleted=False).order_by(Product.id).slice(start, stop), \
            query.filter_by(is_deleted=False).count()

    @staticmethod
    def all_products(records_per_page, page):

        ## put filter here

        stop = page * records_per_page
        start = stop - records_per_page
        return Product.query.filter_by(is_deleted=False).order_by(Product.id).slice(start, stop)


class Dimension(Base):
    __tablename__ = 'dimensions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(10))
    
    def __init__(self, name):
        super(Dimension, self).__init__()
        self.name = name

    def __str__(self):
        return self.name

    @staticmethod
    def get_dimension(id):
        return Dimension.query.get(id)

    @staticmethod
    def add_dimension(name):
        d = Dimension(name)
        db_session.add(d)
        db_session.commit()

    @staticmethod
    def update_dimension(id, new_name):
        entry = Dimension.query.get(id)
        entry.name = new_name
        db_session.commit()

    @staticmethod
    def get_all_dimensions():
        return Dimension.query.all()
#Product.del_product(10)
#print Product.get_product(10)