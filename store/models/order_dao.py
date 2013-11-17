from models import Base, db_session
from sqlalchemy import Column, Integer, String, DATE, ForeignKey, and_
from sqlalchemy.orm import relationship, backref
from models.product_dao import Product
from models.user_dao import UserDao
from datetime import date


class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('UserDao', backref=backref('order', lazy='dynamic'))
    date = Column(DATE, default=date.today())
    status_id = Column(Integer, ForeignKey('order_status.id'))
    status = relationship('OrderStatus', backref=backref('order', lazy='dynamic'))
    delivery_id = Column(Integer, ForeignKey('delivery_type.id'), nullable=True)
    delivery = relationship('DeliveryType', backref=backref('order', lazy='dynamic'))

    def __init__(self, user_id, date, status_id, delivery_id):
        super(Order, self).__init__()
        self.user_id = user_id
        self.date = date
        self.status_id = status_id
        self.delivery_id = delivery_id

    @staticmethod
    def get_order(id):
        return Order.query.get(id)

     # Nex method retrieve list of orders for one user if user_id exist and filter by date if date exist
     # and retrieve list of orders for all user if user_id is None and filter by date if date exist
     # example  get_order_user_id_date ('',date.today()) get_order_user_id_date (1)

    @staticmethod
    def get_order_user_id_date(user_id=None, date=None):
        if date and user_id:
            return Order.query.filter(Order.user_id == user_id).filter(Order.date == date).all()
        elif user_id:
            return Order.query.filter(Order.user_id == user_id).all()
        elif date:
            return Order.query.filter(Order.date == date).all()
        else:
            return Order.query.all()


    @staticmethod
    def add_order(user_id, date, status_id, delivery_id = None):
        order = Order(user_id, date, status_id, delivery_id)
        db_session.add(order)
        db_session.commit()

    @staticmethod
    def update_order(id, new_user_id, new_date, new_status_id, new_delivery_id):
        ord_up = Order.get_order(id)
        ord_up.user_id = new_user_id
        ord_up.date = new_date
        ord_up.status_id = new_status_id
        ord_up.delivery_id = new_delivery_id
        db_session.commit()


    @staticmethod
    def getOrderByStatus(user_id):
        return Order.query.filter(and_(Order.status_id == 'Cart', Order.user_id == user_id)).first()


class OrderStatus(Base):
    __tablename__ = "order_status"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))

    def __init__(self, name):
        super(OrderStatus, self).__init__()
        self.name = name

    # Next method retrieve list of records
    @staticmethod
    def get_status_all():
        return OrderStatus.query.order_by(id).all()

    # Next method retrieve record by id
    @staticmethod
    def get_status(id):
        return OrderStatus.query.get(id)

    @staticmethod
    def add_status(name):
        p = OrderStatus(name)
        db_session.add(p)
        db_session.commit()

    @staticmethod
    def update_status(id, new_name):
        entry = OrderStatus.get_status(id)
        entry.name = new_name
        db_session.commit()

    @staticmethod
    def delete_status(id):
        dele = OrderStatus.get_status(id)
        db_session.delete(dele)
        db_session.commit()


class DeliveryType(Base):
    __tablename__ = "delivery_type"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))

    def __init__(self, name):
        super(DeliveryType, self).__init__()
        self.name = name

    def __str__(self):
        return self.name

    @staticmethod
    def get_delivery(id):
        return DeliveryType.query.get(id)

    @staticmethod
    def get_delivery_all():
        return DeliveryType.query.all()

    @staticmethod
    def add_delivery(name):
        d = DeliveryType(name)
        db_session.add(d)
        db_session.commit()

    @staticmethod
    def update_delivery(id, new_name):
        entry = DeliveryType.get_delivery(id)
        entry.name = new_name
        db_session.commit()

    @staticmethod
    def delete_delivery(id):
        del_delivery = DeliveryType.get_delivery(id)
        db_session.delete(del_delivery)
        db_session.commit()


class OrderProduct(Base):
    __tablename__ = "order_product"
    order_id = Column(Integer, ForeignKey('order.id'), primary_key=True, autoincrement=True)
    order = relationship('Order', backref=backref('order_product', lazy='dynamic'))
    product_id = Column(Integer, ForeignKey('products.id'), primary_key=True)
    product = relationship('Product', backref=backref('order_product', lazy='dynamic'))
    quantity = Column(Integer)


    def __init__(self, order_id, product_id, quantity):
        super(OrderProduct, self).__init__()
        self.quantity = quantity
        self.order_id = order_id
        self.product_id = product_id

    #Next method retrieve one record for composite primary key (order_id, product_id)
    @staticmethod
    def get_order_product(order_id,product_id):
        return OrderProduct.query.get((order_id, product_id))

    @staticmethod
    def get_by_order(product_id):
        return OrderProduct.query.filter(OrderProduct.product_id == product_id).all()

    @staticmethod
    def get_by_product(order_id):
        return OrderProduct.query.filter(OrderProduct.order_id == order_id).all()

    @staticmethod
    def add_order_product(order_id, product_id, quantity):
        order_product = OrderProduct(order_id, product_id, quantity)
        db_session.add(order_product)
        db_session.commit()

    @staticmethod
    def update_order_product(order_id, product_id, new_quantity):
        order_product_up = OrderProduct.get_order_product(order_id, product_id)
        order_product_up.quantity = new_quantity
        db_session.commit()

    @staticmethod
    def delete_order_product(order_id, product_id):
        del_order_product = OrderProduct.get_order_product(order_id, product_id)
        db_session.delete(del_order_product)
        db_session.commit()

    @staticmethod
    def updateSumQuantity(order_id, product_id, new_quantity):
        order_product_up = OrderProduct.get_order_product(order_id, product_id)
        order_product_up.quantity += new_quantity
        db_session.commit()

#b = DeliveryType.get_delivery_all()

#OrderProduct.add_order_product(1,4,5)

#Order.add_order(1,date.today(),2,1)

#for i in b:
#    print i
#
#print (DeliveryType.get_delivery(2))
#print date.today()

#k= OrderProduct.get_order_product(1,7)
#print k.quantity
#
#Order.update_order(1,4,date.today(),1,1)
#print Order.get_order(1).date
#d=date.today()
#order1 = OrderProduct.get_by_order(3)
#
#for i in order1:
#    print i.quantity

