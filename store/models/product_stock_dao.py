#!/usr/bin/env python

from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer,and_

from models import Base, db_session
from sqlalchemy.orm import relationship, backref
from models.order_dao import OrderProduct
from models.product_dao import Dimension, Product


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

    @staticmethod
    def add_new_record(product_id, dimension_id, quantity):
        ps = ProductStock(product_id, dimension_id, quantity)
        db_session.add(ps)
        db_session.commit()

    def __str__(self):
        return "CData  '%s, %s, %s'" % (self.product_id, self.dimension_id, self.quantity)


    @staticmethod
    def addProductStock(product_id, quantity):
        query = Dimension.get_all_dimensions()
        for i in query:
            productStock = ProductStock(product_id, i.id, quantity)
            db_session.add(productStock)
            db_session.commit()

    @staticmethod
    def getProductStock(product_id, dimension_id):
        return ProductStock.query.filter(and_(ProductStock.product_id == product_id,
                                              ProductStock.dimension_id == dimension_id)).first()

    @staticmethod
    def updateProductStock(product_id,dimension_id, new_quantity):
        entry = ProductStock.getProductStock(product_id, dimension_id)
        entry.quantity = new_quantity
        db_session.commit()


    @staticmethod
    def addDimensionStock(dimension_id, quantity):
        query = Product.get_all_products()
        for i in query:
            productStock = ProductStock(i.id, dimension_id, quantity)
            db_session.add(productStock)
            db_session.commit()

    @staticmethod
    def get_quantity_result(product_id,dimension_id,quantity,check):
        i=ProductStock.query.filter(and_(ProductStock.product_id == product_id,ProductStock.dimension_id==dimension_id,\
                                         ProductStock.quantity >= quantity, )).all()
        if i and check=='check':
            return True
        elif i and check =='update':
            i.quantity = i.quantity-quantity
            db_session.commit()
        else:
            False


    def getStockByProduct(product_id):
        return ProductStock.query.filter(ProductStock.product_id == product_id).all()

    @staticmethod
    def getStockByDimension(dimension_id):
        return ProductStock.query.filter(ProductStock.dimension_id == dimension_id).all()

