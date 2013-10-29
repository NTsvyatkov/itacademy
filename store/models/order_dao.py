from models import db ,Base , db_engine
from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, String, DATE
from models.user_dao import User
from models.product_dao import Product
from sqlalchemy.orm import relationship, backref, sessionmaker

import datetime
class Order(db.Model):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(Product.id))
    user_relat = relationship('Product', backref=backref('product', lazy='dynamic'))
    date = Column(DATE)

    #status_id = Column(Integer, ForeignKey('order_status.id'))
   # status = relationship('Order_Status', backref=backref('order', lazy='dynamic'))

    #delivery_id = Column(Integer, ForeignKey('delivery_type.id'))
    #delivery = relationship('Delivery_Type', backref=backref('order', lazy='dynamic'))

    def __init__(self, user_id, date):
        self.user_id = user_id
        self.date = date
        #self.status = status
        #self.delivery_type = delivery_type

    def __str__(self):
        return "OrderData'%s, %s, %s, %s, %s, %s, %s, %s, '" % (self.id,
        self.user_id, self.date)

    @staticmethod
    def add_order(user_id, date):
        ord = Order(user_id, date)
        db.session.add(ord)
        db.session.commit()

db.metadata.create_all()

Order.add_order(1,datetime.datetime.now().date())


