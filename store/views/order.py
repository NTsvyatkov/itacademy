from flask import jsonify, render_template, request, make_response, session, json
from models.order_dao import product_order_update
from flask_bootstrap import app

from models.order_dao import order_product_grid, OrderProduct, DeliveryType


@app.route('/order_product')
def order_grid():
    delivery_list = DeliveryType.get_delivery_all()
    delivery_arr = []
    for i in delivery_list:
        delivery_arr.append({'id': i.id, 'name': i.name})

    order_product = order_product_grid(session['id'])
    if order_product:
        return render_template('order.html',delivery_arr=delivery_arr)
    else:
        return render_template('order_empty.html')


@app.route('/api/order_product', methods=['GET'])
def order():
    if 'user_id' in session:
        order_list = order_product_grid(session['id'])
    else:
        order_list = order_product_grid(4)
    order_arr = []
    for i in order_list:
        order_arr.append({'order_id':i.Order.id, 'id': i.Product.id, 'name': i.Product.name, 'price': i.Product.price,\
         'description': i.Product.description,'quantity':i.OrderProduct.quantity,\
         'dimension':i.OrderProduct.dimension.name,'dimension_id':i.OrderProduct.dimension.id })
    return make_response(jsonify(order=order_arr), 200)


@app.route('/api/order_product/<int:id_product>/<int:id_order>', methods=['DELETE'])
def order_id_delete(id_order,id_product):
    OrderProduct.delete_order_product(id_order,id_product)
    resp = make_response(jsonify({'message': 'success'}), 200)
    return resp


@app.route('/api/order_product', methods=['PUT'])
def order_post():
    js = request.get_json()
    product_order_update(js)
    resp = make_response(jsonify({'message': 'success'}), 200)
    return resp



