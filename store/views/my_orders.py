#!/usr/bin/env python
from flask import render_template, request, make_response, jsonify, session
from flask_bootstrap import app
from models.order_dao import Order,  OrderStatus

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


@app.route('/api/orders/', methods=['GET'])
def ordersPage():
    user_id = session['id']
    records_per_page = int(request.args.get('table_size'))
    page=int(request.args.get('page'))
    prods, records_amount = Order.pagerByFilter(user_id, page, records_per_page)
    orders_list = []
    for i in prods:
        orders_list.append({'date': i.date.strftime("%d/%m/%y"), 'orderStatus': OrderStatus.get_status(i.status_id).name,
                      'amount': '0.00'})
    return make_response(jsonify(orders=orders_list, records_amount=records_amount,
                                 records_per_page=records_per_page), 200)

