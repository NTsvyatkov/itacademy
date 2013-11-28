from models import Base, db_session
from sqlalchemy import Column, Integer, String, DATE, ForeignKey, and_, Boolean, Float, DECIMAL, TEXT
from sqlalchemy.orm import relationship, backref
from models.product_dao import Product
from models.user_dao import UserDao
from datetime import date


class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    #user = relationship('UserDao', backref=backref('order', lazy='dynamic'), foreign_keys=[user_id])
    user = relationship('UserDao', foreign_keys=user_id)
    date = Column(DATE, default=date.today())
    status_id = Column(Integer, ForeignKey('order_status.id'))
    status = relationship('OrderStatus', backref=backref('order', lazy='dynamic'))
    delivery_id = Column(Integer, ForeignKey('delivery_type.id'), nullable=True)
    delivery = relationship('DeliveryType', backref=backref('order', lazy='dynamic'))
    assignee_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    assignee = relationship('UserDao', foreign_keys=[assignee_id])
    total_price = Column(DECIMAL(5,2), nullable=True)
    preferable_delivery_date = Column(DATE, nullable=True)
    delivery_date = Column(DATE, nullable=True)
    gift = Column(Boolean, default=False, nullable=True)
    delivery_address = Column(String(50))
    comment = Column(TEXT)


    def __init__(self, user_id, date,status_id, delivery_id, total_price, assignee_id,
                 preferable_delivery_date, delivery_date, gift, delivery_address, comment ):
        super(Order, self).__init__()
        self.user_id = user_id
        self.date = date
        self.date = date
        self.status_id = status_id
        self.delivery_id = delivery_id
        self.total_price = total_price
        self.assignee_id = assignee_id
        self.preferable_delivery_date = preferable_delivery_date
        self.delivery_date = delivery_date
        self.gift = gift
        self.delivery_address = delivery_address
        self.comment = comment

    @staticmethod
    def get_order(id):
        return Order.query.get(id)


    @staticmethod
    def getAllOrders():
        return Order.query.order_by(Order.id).all()

    @staticmethod
    def get_order_user_id_date(user_id=None, date=None):
        """ Nex method retrieve list of orders for one user if user_id exist and filter by date if date exist
        and retrieve list of orders for all user if user_id is None and filter by date if date exist
        example  get_order_user_id_date ('',date.today()) get_order_user_id_date (1)"""
        if date and user_id:
            return Order.query.filter(Order.user_id == user_id).filter(Order.date == date).all()
        elif user_id:
            return Order.query.filter(Order.user_id == user_id).all()
        elif date:
            return Order.query.filter(Order.date == date).all()
        else:
            return Order.query.all()

    @staticmethod
    def add_order(user_id, date, status_id, delivery_id = None, total_price = None, assignee_id = None,
                  preferable_delivery_date = None, delivery_date=None, gift= None,
                   delivery_address = None, comment =None):
        order = Order(user_id, date, status_id, delivery_id, total_price, assignee_id, preferable_delivery_date,
                      delivery_date, gift,delivery_address,comment)
        db_session.add(order)
        db_session.commit()

    @staticmethod
    def update_order(id, new_user_id, new_date, new_status_id, new_delivery_id,
                     new_total_price, new_preferable_delivery_date, new_delivery_date,
                     new_gift, new_delivery_address, new_comment ):
        ord_up = Order.get_order(id)
        ord_up.user_id = new_user_id
        ord_up.date = new_date
        ord_up.status_id = new_status_id
        ord_up.delivery_id = new_delivery_id
        ord_up.total_price = new_total_price

        ord_up.preferable_delivery_date = new_preferable_delivery_date
        ord_up.delivery_date = new_delivery_date
        ord_up.gift = new_gift
        ord_up.delivery_address = new_delivery_address
        ord_up.comment = new_comment

        db_session.commit()


    @staticmethod
    def getOrderByStatus(user_id):
        return Order.query.filter(and_(Order.status_id == 3, Order.user_id == user_id)).first()

    @staticmethod
    def pagerByFilter(user_id=None, page=None, records_per_page=None):
        query = Order.query.filter(Order.user_id == user_id)
        stop = page * records_per_page
        start = stop - records_per_page
        return query.order_by(Order.id).slice(start, stop), \
            query.count()


    @staticmethod
    def pagerByFilterOrder(status_id=None, assignee_id=None, page=None, records_per_page=None):
        query = Order.query
        if status_id:
            query = query.filter(Order.status_id == status_id)
        if assignee_id:
            query = query.filter(Order.assignee_id == assignee_id)
        stop = page * records_per_page
        start = stop - records_per_page
        return query.order_by(Order.id).slice(start, stop), \
            query.count()

class OrderStatus(Base):
    __tablename__ = "order_status"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))

    def __init__(self, name):
        super(OrderStatus, self).__init__()
        self.name = name


    @staticmethod
    def get_status_all():
        # Next method retrieve list of records
        return OrderStatus.query.order_by(id).all()


    @staticmethod
    def get_status(id):
        # Next method retrieve record by id
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

    @staticmethod
    def get_all_order_status():
        return OrderStatus.query.all()


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
    dimension_id = Column(Integer, ForeignKey('dimensions.id'), primary_key=True)
    dimension = relationship('Dimension', backref=backref('products', lazy='dynamic'))
    quantity = Column(Integer)
    price = Column(DECIMAL, nullable=True)
    #price_id = Column(Integer,ForeignKey('products.price'), nullable=True)
    #price = relationship('Product', backref=backref('order_product', lazy='dynamic'))


    def __init__(self, order_id, product_id, dimension_id, quantity, price):
        super(OrderProduct, self).__init__()
        self.quantity = quantity
        self.order_id = order_id
        self.product_id = product_id
        self.dimension_id = dimension_id
        self.price = price


    @staticmethod
    def get_order_product(order_id,product_id, dimension_id):
        #Next method retrieve one record for composite primary key (order_id, product_id, dimension_id)
        return OrderProduct.query.get((order_id, product_id, dimension_id))

    @staticmethod
    def get_by_order(product_id):
        return OrderProduct.query.filter(OrderProduct.product_id == product_id).all()

    @staticmethod
    def get_by_product(order_id):
        return OrderProduct.query.filter(OrderProduct.order_id == order_id).all()

    @staticmethod
    def add_order_product(order_id, product_id, dimension_id, quantity, price = None):
        order_product = OrderProduct(order_id, product_id, dimension_id, quantity, price)
        db_session.add(order_product)
        db_session.commit()

    @staticmethod
    def update_order_product(order_id, product_id, dimension_id, new_quantity, new_price):
        order_product_up = OrderProduct.get_order_product(order_id, product_id, dimension_id)
        order_product_up.quantity = new_quantity
        order_product_up.price = new_price
        db_session.commit()

    @staticmethod
    def delete_order_product(order_id, product_id, dimension_id):
        del_order_product = OrderProduct.get_order_product(order_id, product_id, dimension_id)
        db_session.delete(del_order_product)
        db_session.commit()

    @staticmethod
    def updateSumQuantity(order_id, product_id, dimension_id, new_quantity):
        order_product_up = OrderProduct.get_order_product(order_id, product_id, dimension_id)
        order_product_up.quantity = new_quantity
        db_session.commit()




def order_product_grid(user_id):
    return db_session.query(OrderProduct, Order, Product).join(Order).join(Product).\
        filter(and_(Order.user_id==user_id ,Order.status_id == 3 )).all()

def product_order_update(dict):

    order_id=int(dict['order_id'])
    amount=0
    get_order = Order.get_order(order_id)
    for i in dict['product_quantity']:
        comment=dict['comment']
        delivery_type=int(dict['delivery_type'])
        dimension=int(i['dimension_id'])
        delivery_address=dict['delivery_address']
        product_id=int(i['product_id'])
        quantity=int(i['quantity'])
        price = Product.get_product(product_id).price

        amount= amount + price*quantity

        total_price = price*quantity
        order_product= OrderProduct.get_order_product(order_id,product_id,dimension)
        order_product.quantity=quantity
        order_product.total_price=total_price
        db_session.commit()


    get_order.status_id = 1
    get_order.delivery_id = delivery_type
    get_order.total_price = amount
    get_order.delivery_address = delivery_address
    get_order.comment = comment
    db_session.commit()

