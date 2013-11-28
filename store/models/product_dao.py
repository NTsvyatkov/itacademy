from models import Base, db_session
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Float, Boolean,and_,or_
from sqlalchemy.orm import relationship, backref


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    description = Column(Text)
    price = Column(Float)
    #dimension_id = Column(Integer, ForeignKey('dimensions.id'))
    #dimension = relationship('Dimension', backref=backref('products', lazy='dynamic'))
    is_deleted = Column(Boolean, default=False)

    def __init__(self, name, description, price, is_deleted=False):
        super(Product, self).__init__()
        self.name = name
        self.description = description
        self.price = price
        self.is_deleted = is_deleted

    def __str__(self):
        return '%s, %s, %s, %s' % (self.name, self.description, self.price, self.is_deleted)

    @staticmethod
    def add_product(name, description, price):
        p = Product(name, description, price)
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
    def upd_product(id, new_name, new_description, new_price):
        entry = Product.get_product(id)
        entry.name = new_name
        entry.description = new_description
        entry.price = new_price
        #entry.dimension = Dimension.query.get(new_dimension)
        db_session.commit()

    @staticmethod
    def get_all_products():
        return Product.query.filter_by(is_deleted=False).all()

    @staticmethod
    def pagerByFilter(name=None, start_price=None, end_price=None, page=None, records_per_page=None):
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
    def filter_product_grid(a_dict, page=None, records_per_page=None):
        """This method exercise filter by filter dictionary in product_grid.html
           filter_description, filter_name  1 = start with
                                            2 = contains
                                            3 = equal to
           filter_price 1 = less than
                         2 = more than
                         3 = equal to
        """
        stop = page * records_per_page
        start = stop - records_per_page

     
        if a_dict['name']:
            filter_name={'1':Product.name.like(a_dict['name']+'%'),\
                         '2':Product.name.like('%'+a_dict['name'])+'%',\
                         '3':Product.name == a_dict['name']}

        if a_dict['description']:
            filter_description={'1':Product.description.like(a_dict['description']+'%'),\
                                '2':Product.description.like('%'+a_dict['description']+'%'),\
                                '3':Product.description == a_dict['description']}
        if a_dict['price']:
            filter_price={'1':Product.price < (a_dict['price']),\
                          '2':Product.price > (a_dict['price']),\
                          '3':Product.price == a_dict['price']}

        query = Product.query
        if a_dict['name']:
            query= query.filter(filter_name[a_dict['name_options']])
        if a_dict['description']:
            query= query.filter(filter_description[a_dict['description_options']])
        if a_dict['price']:
            query= query.filter(filter_price[a_dict['price_options']])
        #elif list['description'] and list['price']:
        #    query= Product.query.filter(and_(filter_description[list['description_options']],\
        #                                     filter_price[list['price_options']]))
        #elif list['name']:
        #    query= Product.query.filter(filter_name[list['name_options']])
        #
        #elif list['description']:
        #    query= Product.query.filter(filter_description[list['description_options']])
        #
        #elif list['price']:
        #    query= Product.query.filter(filter_price[list['price_options']])

        count = query.filter_by(is_deleted=False).count()
        return query.filter_by(is_deleted=False).order_by(Product.id).slice(start, stop).all(), count


class Dimension(Base):
    __tablename__ = 'dimensions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20))
    number = Column(Integer)
    is_deleted = Column(Boolean, default=False)
    
    def __init__(self, name,number , is_deleted=False):
        super(Dimension, self).__init__()
        self.name = name
        self.number = number
        self.is_deleted = is_deleted

    def __str__(self):
        return '%s, %s, %s' % (self.name, self.number, self.is_deleted)

    @staticmethod
    def deleteDimension(id):
        entry = Dimension.get_dimension(id)
        entry.is_deleted = True
        db_session.commit()

    @staticmethod
    def get_dimension(id):
        return Dimension.query.get(id)

    @staticmethod
    def add_dimension(name, number):
        d = Dimension(name, number)
        db_session.add(d)
        db_session.commit()

    @staticmethod
    def update_dimension(id, new_name, new_number):
        entry = Dimension.query.get(id)
        entry.name = new_name
        entry.number = new_number
        db_session.commit()

    @staticmethod
    def get_all_dimensions():
        return Dimension.query.filter_by(is_deleted=False).all()
#Product.del_product(10)
#print Product.get_product(10)
#
#filter_list={
#        'name':'ap','name_options':'1',\
#        'description':'re','description_options':'1',\
#        'price':'1','price_options':'2'}
#
#all_rec , all= Product.filter_product_grid(filter_list,1,3)
#
#for i in all_rec:
#    print i.name
