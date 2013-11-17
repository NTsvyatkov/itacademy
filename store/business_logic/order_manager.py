#!/usr/bin/env python

import re
from validation import ValidationException, NotFoundException
from models.region_dao import RegionDao
from models.role_dao import RoleDao
from models.order_dao import Order


def getListOrder():
    return Order.getAllOrders()

def validate_order_id(id):
    if id is None:
        raise ValidationException("Order id is required field")
    if not Order.get_order(id):
        raise NotFoundException("Unable to find order with given id")

def get_order_by_id(id):
    validate_order_id(id)
    order_by_id = Order.get_order(id)
    return order_by_id