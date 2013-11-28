#!/usr/bin/env python

from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer
from models import Base, db_session
from sqlalchemy.orm import relationship, backref
from models.order_dao import OrderProduct
from models.product_dao import Dimension


class ProductStock(Base):
    __tablename__ = "product_stock"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship('Product', backref=backref('product_stock', lazy='dynamic'))
    dimension_id = Column(Integer, ForeignKey('dimensions.id'))
    dimension = relationship('Dimension', backref=backref('product_stock', lazy='dynamic'))
    quantity = Column(Integer)


    def __init__(self, product_id, dimension_id, quantity):
        super(ProductStock, self).__init__()
        self.product_id = product_id
        self.dimension_id = dimension_id
        self.quantity = quantity


    def __str__(self):
        return "CData  '%s, %s, %s'" % (self.product_id, self.dimension_id, self.quantity)

    @staticmethod
    def addProductStock(product_id):
        query = OrderProduct.query.filter(OrderProduct.product_id == product_id).all()
        for i in query:
            productStock = ProductStock(product_id, i.dimension_id, i.quantity)
            db_session.add(productStock)
            db_session.commit()


    @staticmethod
    def addDimensionStock(dimension_id):
        query = OrderProduct.query.filter(OrderProduct.dimension_id == dimension_id).all()
        for i in query:
            productStock = ProductStock(i.product_id, dimension_id, i.quantity)
            db_session.add(productStock)
            db_session.commit()