from flask import jsonify, render_template, request, make_response, session
from models.product_dao import Product
from flask_bootstrap import app
from maintenance.pager import Pagination
from business_logic.product_manager import list_products, list_dimensions, create_product, delete_product,\
    update_product, get_product_by_id
from models.order_dao import order_product_grid, OrderProduct, DeliveryType



@app.route('/api/order_product', methods=['GET'])
def order():
    if 'user_id' in session:
        order_list = order_product_grid(session['user_id'])
    else:
        order_list = order_product_grid(3)
    order_arr = []
    for i in order_list:
        order_arr.append({'id': i.Product.id, 'name': i.Product.name, 'price': i.Product.price, \
         'description': i.Product.description, 'dimension':i.Product.dimension.name,'quantity':i.OrderProduct.quantity})
    return make_response(jsonify(order=order_arr), 200)


@app.route('/api/order_product/<int:id>', methods=['DELETE'])
def order_id_delete(id):
    OrderProduct.delete_order_product()
    resp = make_response(jsonify({'message': 'success'}), 200)
    return resp


@app.route('/api/order_product', methods=['POST'])
def order_post():
    js = request.get_json()
    create_product(js['name'], js['description'], js['price'], js['id'])
    resp = make_response('', 201)
    return resp


@app.route('/order_product')
def order_grid():
    delivery_list = DeliveryType.get_delivery_all()
    delivery_arr = []
    for i in delivery_list:
        delivery_arr.append({'id': i.id, 'name': i.name})
    return render_template('order.html',dimensions_arr=delivery_arr)
