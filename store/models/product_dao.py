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
    def listFilterBuyProducts(name, start_price, end_price):
        query = Product.query.filter_by(is_deleted=False)
        if name:
            query = query.filter(or_(Product.name == name, Product.description == name))
        if start_price:
            query = query.filter(Product.price >= start_price)
        if end_price:
            query = query.filter(Product.price <= end_price)
        return query.all()

    @staticmethod
    def filter_product_grid(list):
        """This method exercise filter by filter list in product_grid.html
           filter_description, filter_name  1 = start with
                                            2 = contains
                                            3 = equal to
            filter_price 1 = less than
                         2 = more than
                         3 = equal to
        """
        if list['name']:
            filter_name={'1':Product.name.like(list['name']+'%'),\
                         '2':Product.name.like(list['name']),\
                         '3':Product.name == list['name']}

        if list['description']:
            filter_description={'1':Product.description.like(list['description']+'%'),\
                                '2':Product.description.like(list['description']),\
                                '3':Product.description == list['description']}
        if list['price']:
            filter_price={'1':Product.price < (list['price']),\
                          '2':Product.price > (list['price']),\
                          '3':Product.price == list['price']}

        if list['name'] and list['description'] and list['price']:
            return Product.query.filter(and_(filter_name[list['name_options']],\
                                             filter_description[list['description_options']],\
                                             filter_price[list['price_options']])).all()
        elif list['name'] and list['description']:
            return Product.query.filter(and_(filter_name[list['name_options']],\
                                             filter_description[list['description_options']])).all()
        elif list['name'] and list['price']:
            return Product.query.filter(and_(filter_name[list['name_options']],\
                                             filter_price[list['price_options']])).all()
        elif list['description'] and list['price']:
            return Product.query.filter(and_(filter_description[list['description_options']],\
                                             filter_price[list['price_options']])).all()
        elif list['name']:
            return Product.query.filter(filter_name[list['name_options']]).all()

        elif list['description']:
            return Product.query.filter(filter_name[list['description_options']]).all()

        elif list['price']:
            return Product.query.filter(filter_name[list['price_options']]).all()




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
#
#filter_list={'name':'mango','name_options':'2',\
#        'description':'fresh','description_options':'1',\
#        'price':'7.4','price_options':'2'}
#
#all_rec = Product.filter_product_grid(filter_list)
#
#for i in all_rec:
#    print i.name
