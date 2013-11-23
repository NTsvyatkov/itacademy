#!/usr/bin/env python
from datetime import date
from sqlalchemy import and_
from flask import render_template, request, make_response, jsonify, session
from flask_bootstrap import app
from models.order_dao import Order, OrderProduct


@app.route('/product_buy', methods=('GET', 'POST'))
def productBuy():
    return render_template('product_buy.html',)


@app.route('/api/order/product/<int:id>', methods = ['POST'])
def amountProducts(id):
    user_id = session['id']
    json = request.get_json()
    order_status = Order.getOrderByStatus(user_id)
    if order_status is None:
        Order.add_order(user_id,date.today(), 4, )
    #if OrderProduct.query.filter(and_(OrderProduct.product_id == id, OrderProduct.order_id == order.id)):
    order = Order.getOrderByStatus(user_id)
    if  OrderProduct.get_order_product(order.id, id):
        OrderProduct.updateSumQuantity(order.id, id, json['value'])
    else:
        OrderProduct.add_order_product(Order.getOrderByStatus(user_id).id, id, json['value'])
    return make_response(jsonify({'message':'success'}),200)