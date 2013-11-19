from models.order_dao import Order
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
        return (Order.query.order_by(Order.user_id).slice(self.start-1, self.start)).count() > 0

    @property
    def has_next(self):
        return (Order.query.order_by(Order.user_id).slice(self.stop, self.stop+1)).count() > 0

    @property
    def prev_num(self):
        return self.page - 1

    @property
    def next_num(self):
        return self.page + 1

    def pager(self):
        return Order.query.order_by(Order.user_id).slice(self.start, self.stop)
