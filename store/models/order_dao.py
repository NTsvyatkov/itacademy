from models import Base, db_session, engine
from sqlalchemy import Column, Date, Integer, String, DATE, ForeignKey, Text, Float
from sqlalchemy.orm import relationship, backref
from models.product_dao import Product
from models.user_dao import UserDao


Base.query = db_session.query_property()
class Order(Base):
    
    __tablename__ = "order"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('UserDao', backref=backref('order', lazy='dynamic'))
    date = Column(DATE)
    status_id = Column(Integer,ForeignKey('order_status.id'))
    status = relationship('Order_Status', backref=backref('order', lazy='dynamic'))
    delivery_id = Column(Integer,ForeignKey('delivery_type.id'))
    delivery = relationship('Delivery_Type', backref=backref('order', lazy='dynamic'))
	
    def __init__(self,  user_id,date,status_id,delivery_id):  # ??????
        self.user_id=user_id
        self.date=date
        self.status_id=status_id
        self.delivery_id=delivery_id
        
    @staticmethod
    def get_order(id):
        return db_session.query(Order).get(id)

    @staticmethod
    def get_order_user_id_date(user_id=None, date=None):
        if (date != None) and (user_id != None):
            return db_session.query(Order).filter(user_id==user_id).filter(date==date).all()
        elif user_id != None:
            return db_session.query(Order).filter(user_id==user_id).all()
        elif date != None:
            return db_session.query(Order).filter(date==date).all()
        else:
            return db_session.query(Order).all()

        
    @staticmethod
    def add_order(user_id,date,status_id,delivery_id):
        order = Order(user_id,date,status_id,delivery_id)
        db_session.add(order)
        db_session.commit()

    @staticmethod
    def update_order(id, new_user_id, new_date, new_status_id, new_delivery_id):
        ordup = Order.get_order(id)
        ordup.user_id = new_user_id
        ordup.date = new_date
        ordup.status_id = new_status_id
        ordup.delivery_id = new_delivery_id
        db_session.commit()
        

class Order_Status(Base):

    __tablename__ = "order_status"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))

    def __init__(self, name):
        self.name = name
      
    @staticmethod
    def get_status_all():
        return db_session.query(Order_Status).order_by(id).all()

    @staticmethod
    def get_status(id):
        return db_session.query(Order_Status).get(id)

    @staticmethod
    def add_status(name):
        p = Order_Status(name)
        db_session.add(p)
        db_session.commit()

    @staticmethod
    def update_status(id, new_name):
        entry = Order_Status.get_status(id)
        entry.name = new_name
        db_session.commit()

    @staticmethod
    def delete_status(id):
        dele = Order_Status.get_status(id)
        db_session.delete(dele)
        db_session.commit()


class Delivery_Type(Base):
    __tablename__ = "delivery_type"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    @staticmethod
    def get_delivery(id):
        return Delivery_Type.query.get(id)

    @staticmethod
    def get_delivery_all():
        return Delivery_Type.query.all()

    @staticmethod
    def add_delivery(name):
        d = Delivery_Type(name)
        db_session.add(d)
        db_session.commit()

    @staticmethod
    def update_delivery(id, new_name):
        entry = Delivery_Type.get_delivery(id)
        entry.name = new_name
        db_session.commit()

    @staticmethod
    def delete_delivery(id):
        dele = Delivery_Type.get_delivery(id)
        db_session.delete(dele)
        db_session.commit()


class Order_Product(Base):
    __tablename__ = "order_product"
    order_id = Column(Integer, ForeignKey('order.id'), primary_key=True, autoincrement=True)
    order = relationship('Order', backref=backref('order_product', lazy='dynamic'))
    product_id = Column(Integer, ForeignKey('products.id'), primary_key=True)
    product = relationship('Product', backref=backref('order_product', lazy='dynamic'))
    quantity = Column(Integer)

    def __init__(self, order_id, product_id, quantity):   # ??????
        self.quantity = quantity
        self.order_id = order_id
        self.product_id = product_id

    @staticmethod
    def get_order_product(product_id=None, order_id=None):
        if product_id != None:
            return db_session.query(Order_Product).get(product_id)
        elif order_id != None:
            return db_session.query(Order_Product).get(order_id)

    @staticmethod
    def get_by_order(product_id):
        return db_session.query(Order_Product).filter(product_id == product_id).all()

    @staticmethod
    def get_by_product(order_id):
        return db_session.query(Order_Product).filter(order_id == order_id).all()

    @staticmethod
    def add_order_product(quantity):  # ??????
        op = Order_Product(quantity)
        db_session.add(op)
        db_session.commit()

    @staticmethod
    def update_order_product(id, new_quantity):
        op_up = Order_Product.get_order_product(id)
        op_up.quantity = new_quantity
        db_session.commit()

    @staticmethod
    def delete_order_product(id):
        dele = Order_Product.get_order_product(id)
        db_session.delete(dele)
        db_session.commit()



#Delivery_Type.add_delivery('Fast delivery')
#Delivery_Type.add_delivery('Slow delivery')

b = Delivery_Type.get_delivery_all()

for i in b:
    print i




print (Delivery_Type.get_delivery(2))
