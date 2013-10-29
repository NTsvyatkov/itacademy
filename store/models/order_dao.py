from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, DATE
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///', echo=True)
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column (String(50))

class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    price = Column(Integer)

class Order(Base):
    
    __tablename__ = "order"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', backref=backref('order', lazy='dynamic'))
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
        return session.query(Order).get(id)

	@staticmethod
	def get_order_userid(user_id,date):
        if date != '':
		  return session.query(Order).filter(user_id==user_id).filter(date==date).all()
        else:
            return session.query(Order).filter(user_id==user_id).all()
        
    @staticmethod
    def add_order(user_id,date,status_id,delivery_id):
        order = Order(user_id,date,status_id,delivery_id)
        session.add(order)
        session.commit()

    @staticmethod
    def update_order(id, new_user_id, new_date, new_status_id, new_delivery_id):
        ordup = Order.get_order(id)
        ordup.user_id = new_user_id
        ordup.date = new_date
        ordup.status_id = new_status_id
        ordup.delivery_id = new_delivery_id
        session.commit()
        

class Order_Status(Base):

      __tablename__ = "order_status"
      id = Column(Integer, primary_key=True)
      name = Column(String(50))

      def __init__(self, name):
	  self.name = name
      
      @staticmethod
      def get_status_all():
	      return session.query(Order_Status).order_by(id).all()

      @staticmethod
      def get_status(id):
	      return session.query(Order_Status).get(id)

      @staticmethod
      def add_status(name):
	      p = Order_Status(name)
	      session.add(p)
	      session.commit()

      @staticmethod
      def update_status(id, new_name):
	      entry = Order_Status.get_status(id)
	      entry.name = new_name
	      session.commit()

      @staticmethod
      def delete_status(id):
	      dele = Order_Status.get_status(id)
	      session.delete(dele)
	      session.commit()


class Delivery_Type(Base):

        __tablename__ = "delivery_type"
        id = Column(Integer, primary_key=True)
        name = Column(String(50))

        def __init__(self, name):
            self.name = name

        def __str__(self):
            return self.name

        @staticmethod
        def get_delivery(id):
            return session.query(Delivery_Type).get(id)

        @staticmethod
        def get_delivery_all():
            return session.query(Delivery_Type).all()

        @staticmethod
        def add_delivery(name):
            d = Delivery_Type(name)
            session.add(d)
            session.commit()

        @staticmethod
        def update_delivery(id, new_name):
            entry = Delivery_Type.get_delivery(id)
            entry.name = new_name
            session.commit()

        @staticmethod
        def delete_delivery(id):
            dele= Delivery_Type.get_delivery(id)
            session.delete(dele)
            session.commit()

class Order_Product(Base):

        __tablename__ = "order_product"
        order_id = Column(Integer, ForeignKey('order.id'), primary_key=True)
        order = relationship('Order', backref=backref('order_product', lazy='dynamic'))
        product_id = Column(Integer, ForeignKey('product.id'), primary_key=True)
        product = relationship('Product', backref=backref('order_product', lazy='dynamic'))
        quantity = Column(Integer)

        def __init__(self,order_id,product_id,quantity):   # ??????
            self.quantity=quantity
            self.order_id=order_id
            self.product_id=product_id

        @staticmethod
        def get_order_product(id):
            return session.query(Order_Product).get(id)

        @staticmethod
        def add_order_product(quantity):  # ??????
            op = Order_Product(quantity)
            session.add(op)
            session.commit()

        @staticmethod
        def update_order_product(id, new_quantity):
            op_up = Order_Product.get_order_product(id)
            op_up.quantity = new_quantity
            session.commit()

        @staticmethod
        def delete_order_product(id):
            dele= Order_Product.get_order_product(id)
            session.delete(dele)
            session.commit()

            

Base.metadata.create_all(engine)

#Delivery_Type.add_delivery('Fast delivery')
#Delivery_Type.add_delivery('Slow delivery')

#b = Delivery_Type.get_delivery_all()

#for i in b:
#    print i



#Delivery_Type.delete_delivery(1)

#print (Delivery_Type.get_delivery(2))