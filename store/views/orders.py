#!/usr/bin/env python
from flask import render_template, request, make_response, jsonify, session
from flask_bootstrap import app
from models.order_dao import Order,  OrderStatus
from maintenance.pager_by_orders import Pagination

@app.route('/my_orders')
def  my_orders():
    return render_template('my_orders.html',)

#@app.route('/api/orders', methods=['GET'])
#def order():
#    list = Order.query.order_by(Order.id).all()
#
#    array = []
#    for i in list:
#        array.append({'date': i.date.strftime("%d/%m/%y"), 'orderStatus': OrderStatus.get_status(i.status_id).name,
#                      'amount': i.delivery_id})
#    return make_response(jsonify(products=array), 200)


@app.route('/api/orders/<int:page>', methods=['GET'])
def ordersPage(page):
    all_rec = Order.query.order_by(Order.id).all()
    records_per_page = 5
    pagination = Pagination(records_per_page, all_rec, page)
    prods = pagination.pager()
    records_amount = len(all_rec)
    orders_list = []
    for i in prods:
        orders_list.append({'date': i.date.strftime("%d/%m/%y"), 'orderStatus': OrderStatus.get_status(i.status_id).name,
                      'amount': i.delivery_id})
    return make_response(jsonify(orders=orders_list, records_amount=records_amount,
                                 records_per_page=records_per_page), 200)

