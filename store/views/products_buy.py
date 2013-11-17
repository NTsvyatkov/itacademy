#!/usr/bin/env python
from datetime import date
from flask import render_template, request, make_response, jsonify, session
from flask_bootstrap import app
from models.order_dao import Order, OrderProduct


@app.route('/product_buy', methods=('GET', 'POST'))
def product_buy():
        return render_template('product_buy.html',)


@app.route('/api/order/product/<int:id>', methods = ['POST'])
def amountProducts(id):
    user_id = 2  #session['id']
    order = Order.getOrderByStatus(user_id)
    if order is not None:
        OrderProduct.updateSumQuantity(order.id, id, request.get_json('value'))
    else:
        Order.add_order(user_id,date.today(), 4, )
        OrderProduct.add_order_product(Order.getOrderByStatus(user_id).id, id, request.get_json('value'))
    return make_response(jsonify({'message':'success'}),200)

