#!/usr/bin/env python
from datetime import date
from flask import render_template, request, make_response, jsonify, session
from business_logic.product_manager import list_products
from maintenance.pager import Pagination
from flask_bootstrap import app
from models.order_dao import Order, OrderProduct
from models.product_dao import Product
from models.user_dao import UserDao


@app.route('/api/order/product/<int:id>', methods = ['POST'])
def amountProducts(id):
    user_id = 2  #session['id']
    order = Order.getOrderByStatus(user_id)
    if order is not None:
        OrderProduct.updateSumQuantity(order.id, id, request.get_json('value'))
    else:
        Order.add_order(user_id,date.today(),'Cart', )
        OrderProduct.add_order_product(Order.getOrderByStatus(user_id).id, id, request.get_json('value'))
    return make_response(jsonify({'message':'success'}),200)


#@app.route('/api/product', methods = ['GET'])
#def filterBuyProducts():
#    list = Product.listFilterBuyProducts((request.args.get('name')),(request.args.get('start_price')),
#                                         (request.args.get('end_price')))
#    array = []
#    for i in list:
#        array.append({'id':i.id,'name':i.name,'price':i.price, 'description':i.description})
#    return make_response(jsonify(products=array),200)



#@app.route('/buygrid')
#@app.route('/buygrid/<int:page>')
#def buyProducts(page=1):
#    all_rec = list_products()
#    pagination = Pagination(5, all_rec, page)
#    products = pagination.pager()
#    return render_template('product_buy.html', products=products, pagination=pagination)
#