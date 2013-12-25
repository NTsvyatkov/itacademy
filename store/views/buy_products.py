#!/usr/bin/env python
from flask import render_template, request, make_response, jsonify, session
from business_logic.product_manager import list_dimensions
from flask_bootstrap import app
from business_logic.order_manager import addOrderWithStatusCart, addProductToCartStatus, listOrderProductByOrderId
from models.order_dao import Order, OrderProduct, OrderStatus
from models.product_dao import Product
from business_logic.product_manager import validate_quantity


@app.route('/product_buy', methods=('GET', 'POST'))
def buyProducts():
     if session['role'] not in 'Customer':
        return "You've got permission to access this page."
     else:
        return render_template('buy_product.html',)

@app.route('/api/product', methods=['GET'])
def productsPage():
    name = request.args.get('name')
    start_price = request.args.get('start_price')
    end_price = request.args.get('end_price')
    records_per_page = int(request.args.get('table_size'))
    page = int(request.args.get('page'))
    sort_by = request.args.get('sort_by')
    index_sort = request.args.get('index_sort')
    prods, records_amount = Product.listProducts(name, start_price, end_price, page, sort_by, index_sort, records_per_page)
    products_arr = []
    for i in prods:
        products_arr.append({'id': i.id, 'name': i.name, 'price': str(i.price), 'description': i.description})
    status_list = list_dimensions()
    status_arr = []
    for i in status_list:
        status_arr.append({'id': i.id, 'name': i.name})
    return make_response(jsonify(products=products_arr,status=status_arr, records_amount=records_amount,
                                 records_per_page=records_per_page), 200)

@app.route('/api/order/product/<int:id>', methods = ['POST'])
def buyProduct(id):
    user_id = session['user_id']
    json = request.get_json()
    validate_quantity(id, json['status'], json['value'], 'check')
    addOrderWithStatusCart(user_id)
    addProductToCartStatus(user_id, id, json['status'], json['value'], json['price'])
    return make_response(jsonify({'message':'success'}),200)

@app.route('/api/modal_product', methods=['GET'])
def modalProducts():
    user_id = session['user_id']
    order = Order.getOrderByStatus(user_id)
    products_arr = []
    for i in listOrderProductByOrderId(order.id):
        products_arr.append({'product_id': i.product_id, 'product_name': i.product.name, 'dimension': i.dimension.name,
                             'dimension_id': i.dimension_id, 'quantity': i.quantity, 'price': str(i.price)})
    return make_response(jsonify(products=products_arr), 200)

@app.route('/api/order_product/', methods=['DELETE'])
def deleteOrderProduct():
    order = Order.getOrderByStatus(session['user_id'])
    OrderProduct.delete_order_product(order.id, request.args.get('product_id'), request.args.get('dimension_id'))
    return make_response(jsonify({'message': 'success'}), 200)

@app.route('/api/update_product', methods = ['PUT'])
def updateOrderProduct():
    total_price = 0
    order = Order.getOrderByStatus(session['user_id'])
    for i in OrderProduct.listOrderProductById(order.id):
        total_price += i.price*i.quantity
    Order.updateOrderStatus(order.id, OrderStatus.getNameStatus('Created').id, total_price)
    return make_response(jsonify({'message':'success'}),200)
