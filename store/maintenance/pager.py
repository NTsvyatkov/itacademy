from sqlalchemy import or_
from models.order_dao import Order
from models.product_dao import Product
from math import ceil

class Pagination(object):
    def __init__(self, per_page, all_records, page=1):
        self.page = page
        self.per_page = per_page
        self.stop = self.page * self.per_page
        self.start = self.stop - self.per_page
        self.all_records = all_records

    @property
    def pages(self):
        return int(ceil(len(self.all_records)/float(self.per_page)))

    @property
    def has_prev(self):
        if self.page == 1:
            return False
        return (Product.query.order_by(Product.name).slice(self.start-1, self.start)).count() > 0

    @property
    def has_next(self):
        return (Product.query.order_by(Product.name).slice(self.stop, self.stop+1)).count() > 0

    @property
    def prev_num(self):
        return self.page - 1

    @property
    def next_num(self):
        return self.page + 1

    def pager(self):
        return Product.query.filter_by(is_deleted=False).order_by(Product.id).slice(self.start, self.stop)

    def pagerByFilter(self, name, start_price, end_price):
        query = Product.query.filter_by(is_deleted=False)
        if name:
            query = query.filter(or_(Product.name == name, Product.description == name))
        if start_price:
            query = query.filter(Product.price >= start_price)
        if end_price:
            query = query.filter(Product.price <= end_price)
        return query.filter_by(is_deleted=False).order_by(Product.id).slice(self.start, self.stop)



