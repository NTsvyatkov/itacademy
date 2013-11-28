#!/usr/bin/env python

import re
from datetime import date
from validation import ValidationException, NotFoundException
from models.region_dao import RegionDao
from models.role_dao import RoleDao
from models.order_dao import Order, OrderStatus, DeliveryType, OrderProduct


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

def list_status():
        s_list = OrderStatus.get_all_order_status()
        return s_list

def list_delivery():
        del_list = DeliveryType.get_delivery_all()
        return del_list

def list_assignee():
        assignee_list = RoleDao.query.all()
        return assignee_list


def addOrderWithStatusCart(user_id):
    if Order.getOrderByStatus(user_id) is None:
        Order.add_order(user_id,date.today(), 3)

def addProductToCartStatus(user_id, id, json):
    order = Order.getOrderByStatus(user_id)
    if  OrderProduct.get_order_product(order.id, id,json['status']):
        OrderProduct.updateSumQuantity(order.id, id,json['status'], json['value'])
    else:
        OrderProduct.add_order_product(order.id, id,json['status'], json['value'])

def update_orders(id, new_user_id, new_date, new_status_id, new_delivery_id,
                     new_total_price, new_preferable_delivery_date, new_delivery_date,
                     new_gift, new_delivery_address, new_comment):
    Order.update_order(id, new_user_id, new_date, new_status_id, new_delivery_id,
                     new_total_price, new_preferable_delivery_date, new_delivery_date,
                     new_gift, new_delivery_address, new_comment)
