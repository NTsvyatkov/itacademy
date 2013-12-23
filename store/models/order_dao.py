from models import Base, db_session
from sqlalchemy import Column, Integer, String, DATE, ForeignKey, and_, Boolean, Float, DECIMAL, TEXT, or_, asc, \
                       desc, DDL, event
from sqlalchemy.orm import relationship, backref
from models.product_dao import Product, Dimension
from models.product_stock_dao import ProductStock
from models.user_dao import UserDao
from models.role_dao import RoleDao
from datetime import date
from user_dao import UserLevel


class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('UserDao', foreign_keys=user_id)
    date = Column(DATE, default=date.today())
    status_id = Column(Integer, ForeignKey('order_status.id'))
    status = relationship('OrderStatus', backref=backref('order', lazy='dynamic'))
    delivery_id = Column(Integer, ForeignKey('delivery_type.id'), nullable=True)
    delivery = relationship('DeliveryType', backref=backref('order', lazy='dynamic'))
    assignee_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    assignee = relationship('UserDao', foreign_keys=[assignee_id])
    total_price = Column(DECIMAL(5,2), default=0)
    preferable_delivery_date = Column(DATE, nullable=True)
    delivery_date = Column(DATE, nullable=True)
    gift = Column(Boolean, default=False, nullable=True)
    delivery_address = Column(String(50))
    comment = Column(TEXT)
    order_number=Column(String(6), unique=True)
    discount=Column(Integer, default=0, nullable=True)


    def __init__(self, user_id, date,status_id, delivery_id, total_price, assignee_id,
                 preferable_delivery_date, delivery_date, gift, delivery_address, comment,order_number,discount):
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
        self.order_number=order_number
        self.discount=discount

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
                   delivery_address = None, comment =None,order_number=None, discount=None):
        order = Order(user_id, date, status_id, delivery_id, total_price, assignee_id, preferable_delivery_date,
                      delivery_date, gift,delivery_address,comment,order_number,discount)
        db_session.add(order)
        db_session.commit()
        db_session.refresh(order)
        return order.id

    @staticmethod
    def update_order(id, new_user_id, new_date, new_status_id, new_delivery_id,
                     new_total_price, new_preferable_delivery_date, new_delivery_date,
                     new_gift, new_delivery_address, new_comment, new_order_number, new_discount):
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
        ord_up.new_order_number=new_order_number
        ord_up.new_discount=new_discount

        db_session.commit()

    @staticmethod
    def add_order_number(user_id,order_number):
        if Order.query.filter(Order.order_number == order_number).count() == 0:
            order_id = Order.add_order(user_id,date.today(),3,None,None,None,None,None,None,None,None,order_number,None)
            return order_id
        else:
            return False

    @staticmethod
    def update_current_order(id,new_status_id, new_delivery_id=None, new_delivery_address=None, new_comment=None):
        entry = Order.get_order(id)
        entry.status_id = new_status_id
        entry.delivery_id = new_delivery_id
        entry.delivery_address = new_delivery_address
        entry.comment = new_comment
        db_session.commit()

    @staticmethod
    def update_order_details(id, gift, status, delivery_date):
        order = Order.get_order(id)
        order_status = OrderStatus.query.filter(OrderStatus.name == status).first()
        order.gift = gift
        order.status = order_status
        order.status_id = order_status.id
        order.delivery_date = delivery_date
        db_session.commit()

    @staticmethod
    def getOrderByStatus(user_id):
        return Order.query.filter(and_(Order.status_id == OrderStatus.getNameStatus('Cart').id,
                                       Order.user_id == user_id)).first()

    @staticmethod
    def listOrders(user_id=None, page=None, records_per_page=None, sort_by=None, index_sort=None, filter=None):
        stop = page * records_per_page
        start = stop - records_per_page
        order = asc if index_sort == "asc" else desc
        query = Order.query.outerjoin(Order.assignee, Order.status).filter(and_(Order.user_id == user_id,
                                                             Order.status_id != OrderStatus.getNameStatus('Cart').id))
        if filter['status_option']:
            filterStatus={'0': Order.id,
                    '1': Order.status_id == OrderStatus.getNameStatus('Created').id,
                    '2': Order.status_id == OrderStatus.getNameStatus('Pending').id,
                    '3': Order.status_id == OrderStatus.getNameStatus('Ordered').id,
                    '4': Order.status_id == OrderStatus.getNameStatus('Delivered').id}
            query = query.filter(filterStatus[filter['status_option']])
        if int(filter['order_option']) == 0:
            query = query.filter(Order.id.like(filter['name']+'%'))
        if int(filter['order_option']) == 1:
            query = query.filter(or_(UserDao.first_name.like(filter['name']+'%'),
                                     UserDao.last_name.like(filter['name']+'%')))
        if sort_by == "order_id":
            query = query.order_by(order(Order.id))
        elif sort_by == "order_number":
            query = query.order_by(order(Order.order_number))
        elif sort_by == "total_price":
            query = query.order_by(order(Order.total_price))
        elif sort_by == "max_discount":
            query = query.order_by(order(Order.discount))
        elif sort_by == "delivery_date":
            query = query.order_by(order(Order.delivery_date))
        elif sort_by == "status":
            query = query.order_by(order(OrderStatus.name))
        elif sort_by == "assignee":
            query = query.order_by(order(UserDao.first_name))
        elif sort_by == "role":
            query = query.order_by(order(RoleDao.name))
        return query.order_by(Order.id).slice(start, stop), \
            query.count()

    @staticmethod
    def deleteOrder(orderId):
        removeOrder = Order.get_order(orderId)
        db_session.delete(removeOrder)
        db_session.commit()

    @staticmethod
    def pagerByFilterByMerchandiser(user_id=None, page=None,  records_per_page=None, sort_by=None,
                                    order_sort_by=None, filter=None):
        stop = page * records_per_page
        start = stop - records_per_page
        order = asc if order_sort_by == "asc" else desc
        query = Order.query.outerjoin(Order.user).join(OrderStatus).join(RoleDao).\
                filter(and_(Order.assignee_id == user_id,Order.status_id != OrderStatus.getNameStatus('Cart').id))
        if int(filter['status_option']):
            filterStatus={'1': Order.status_id == OrderStatus.getNameStatus('Pending').id,
                    '2': Order.status_id == OrderStatus.getNameStatus('Ordered').id,
                    '3': Order.status_id == OrderStatus.getNameStatus('Delivered').id}
            query = query.filter(filterStatus[filter['status_option']])
        if filter['name']:
            if int(filter['order_option']) == 0:
                query = query.filter(Order.order_number.like(filter['name']+'%'))
            elif int(filter['order_option']) == 1:
                query = query.filter(or_(UserDao.first_name.like(filter['name']+'%'),
                                         UserDao.last_name.like(filter['name']+'%')))

        if sort_by == "order_id":
            query = query.order_by(order(Order.id))
        elif sort_by == "order_number":
            query = query.order_by(order(Order.order_number))
        elif sort_by == "user":
            query = query.order_by(order(UserDao.first_name))
        elif sort_by == "orderStatus":
            query = query.order_by(order(OrderStatus.name))
        elif sort_by == "total_price":
            query = query.order_by(order(Order.total_price))
        elif sort_by == "role":
            query = query.order_by(order(RoleDao.name))
        return query.order_by(Order.id).slice(start, stop), query.count()

    @staticmethod
    def update_order_number(id,order_number):
        order = Order.get_order(id)
        if Order.query.filter(Order.order_number == order_number).count() == 0:
            order.order_number = order_number
            db_session.commit()
            return True
        else:
            return False

    #Set new new value of level for user, using order id
    @staticmethod
    def set_user_level(order_id):

        order = Order.query.get(order_id)
        if not order.user.balance:
            order.user.balance = order.total_price
        else:
            order.user.balance += order.total_price
        user_status = UserLevel.query.filter(UserLevel.balance < order.user.balance).\
                      order_by(desc(UserLevel.balance)).first()
        order.user.level_id = user_status.id

        db_session.commit()


class OrderStatus(Base):
    __tablename__ = "order_status"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True)

    def __init__(self, name):
        super(OrderStatus, self).__init__()
        self.name = name


    @staticmethod
    def get_status_all():
        # Next method retrieve list of records
        return OrderStatus.query.order_by(id).all()

    @staticmethod
    def getNameStatus(name):
        return OrderStatus.query.filter(OrderStatus.name == name).first()

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
        return OrderStatus.query.all


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
    order_id = Column(Integer, ForeignKey('order.id', ondelete='CASCADE'), primary_key=True, autoincrement=True)
    order = relationship('Order', backref=backref('order_product', lazy='dynamic', passive_deletes=True))
    product_id = Column(Integer, ForeignKey('products.id'), primary_key=True)
    product = relationship('Product', backref=backref('order_product', lazy='dynamic'))
    dimension_id = Column(Integer, ForeignKey('dimensions.id'), primary_key=True)
    dimension = relationship('Dimension', backref=backref('products', lazy='dynamic'))
    quantity = Column(Integer)
    price = Column(DECIMAL(5, 2), nullable=True)
    trigger_status = Column(Boolean, default=False)


    def __init__(self, order_id, product_id, dimension_id, quantity, price, trigger_status = False):
        super(OrderProduct, self).__init__()
        self.quantity = quantity
        self.order_id = order_id
        self.product_id = product_id
        self.dimension_id = dimension_id
        self.price = price
        self.trigger_status = trigger_status

    @property
    def product_price_per_line(self):
        dimension = Dimension.get_dimension(self.dimension_id)
        return self.price * self.quantity * dimension.number

    @staticmethod
    def get_order_product(order_id,product_id, dimension_id):
        #Next method retrieve one record for composite primary key (order_id, product_id, dimension_id)
        return OrderProduct.query.get((order_id, product_id, dimension_id))

    @staticmethod
    def get_by_order(product_id):
        return OrderProduct.query.filter(OrderProduct.product_id == product_id).all()

    @staticmethod
    def get_by_order_product(order_id, page=None, records_per_page=None, sort_by=None, order_sort_by=None):
        stop = page * records_per_page
        start = stop - records_per_page
        order = asc if order_sort_by == "asc" else desc
        count = OrderProduct.query.filter(OrderProduct.order_id == order_id).count()
        query = OrderProduct.query.join(OrderProduct.product).join(OrderProduct.dimension).\
            filter(OrderProduct.order_id == order_id)
        if sort_by == "product_id":
            query = query.order_by(order(OrderProduct.product_id))
        elif sort_by == "product_name":
            query = query.order_by(order(Product.name))
        elif sort_by == "product_description":
            query = query.order_by(order(Product.description))
        elif sort_by == "product_dimension":
            query = query.order_by(order(Dimension.name))
        elif sort_by == "price":
            query = query.order_by(order(OrderProduct.price))
        elif sort_by == "quantity":
            query = query.order_by(order(OrderProduct.quantity))
        elif sort_by == "product_price_per_line":
            query = query.order_by(order(OrderProduct.product_price_per_line))
        return query.slice(start, stop).all(), count

    @staticmethod
    def add_order_product(order_id, product_id, dimension_id, quantity, price = None):
        order_product = OrderProduct(order_id, product_id, dimension_id, quantity, price)
        db_session.add(order_product)
        db_session.commit()

    @staticmethod
    def changeTriggerStatus(order_id, product_id, dimension_id):
        entry = OrderProduct.get_order_product(order_id, product_id, dimension_id)
        entry.trigger_status = True
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
        if del_order_product:
            db_session.delete(del_order_product)
            db_session.commit()

    @staticmethod
    def updateSumQuantity(order_id, product_id, dimension_id, new_quantity):
        order_product_up = OrderProduct.get_order_product(order_id, product_id, dimension_id)
        order_product_up.quantity = int(order_product_up.quantity) + int(new_quantity)
        db_session.commit()

    @staticmethod
    def get_items_quantity(order_id):
        order = OrderProduct.query.filter(OrderProduct.order_id == order_id).all()
        items = 0
        for i in order:
            entry = i.dimension.number*i.quantity
            items = items+entry
        return items

def order_product_grid(user_id,order_id, page=None, records_per_page=None):
    query = db_session.query(OrderProduct, Order, Product).join(Order).join(Product).filter(Order.id==order_id).\
            filter(Order.user_id==user_id).filter((Order.status_id == 3)|(Order.status_id == 4))
    count = query.filter_by(is_deleted=False).count()
    if page and records_per_page:
        stop = page * records_per_page
        start = stop - records_per_page
        return query.slice(start, stop).all(), count
    else:
        return query.all(),count

tbl = OrderProduct.__table__
event.listen(tbl, 'after_create', DDL("""
    CREATE TRIGGER order_product_trigger_update BEFORE UPDATE ON order_product
    FOR EACH ROW BEGIN
        if NEW.trigger_status = True THEN
            UPDATE product_stock SET product_stock.quantity=product_stock.quantity - NEW.quantity WHERE
             product_stock.product_id=NEW.product_id AND product_stock.dimension_id=NEW.dimension_id;
        END IF;
    END;
    """).execute_if(dialect='mysql'))

event.listen(tbl, 'after_create', DDL("""
    CREATE TRIGGER order_product_trigger_delete AFTER DELETE ON order_product
    FOR EACH ROW BEGIN
        if OLD.trigger_status = True THEN
            UPDATE product_stock SET product_stock.quantity=product_stock.quantity + OLD.quantity WHERE
            product_stock.product_id=OLD.product_id AND product_stock.dimension_id=OLD.dimension_id;
        END IF;
    END;
    """).execute_if(dialect='mysql'))
