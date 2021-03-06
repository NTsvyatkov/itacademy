from models import Base, db_session
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DECIMAL, Boolean, and_, or_, asc, desc
from sqlalchemy.orm import relationship, backref


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    description = Column(Text)
    price = Column(DECIMAL(5, 2))
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
        db_session.commit()

    @staticmethod
    def get_all_products():
        return Product.query.filter_by(is_deleted=False).all()

    @staticmethod
    def listProducts(name=None, start_price=None, end_price=None, page=None, sort_by=None, index_sort=None,
                     records_per_page=None):
        product_index = asc if index_sort == "asc" else desc
        query = Product.query.filter_by(is_deleted=False)
        if name:
            query = query.filter(or_(Product.name == name, Product.description == name))
        if start_price:
            query = query.filter(Product.price >= start_price)
        if end_price:
            query = query.filter(Product.price <= end_price)
        stop = page * records_per_page
        start = stop - records_per_page
        if sort_by == "product_name":
            query = query.order_by(product_index(Product.name))
        elif sort_by == "description":
            query = query.order_by(product_index(Product.description))
        elif sort_by == "price":
            query = query.order_by(product_index(Product.price))
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
                         '2':Product.name.like('%'+a_dict['name']+'%'),\
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

        count = query.filter_by(is_deleted=False).count()
        return query.filter_by(is_deleted=False).order_by(Product.id).slice(start, stop).all(), count



    @staticmethod
    def pagerByFilterItem(name=None):
        query = Product.query.filter_by(is_deleted=False)
        if name:
            query = query.filter(or_(Product.name == name, Product.description == name))

        return query.filter_by(is_deleted=False).order_by(Product.id)



    @staticmethod
    def FilterItems(name=None, product_option=None):
        query = Product.query
        if product_option==0:
             query = query.filter(Product.name == name),
        if product_option==0:
            query = query.filter(Product.description == name)
        return query.order_by(Product.id)



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
