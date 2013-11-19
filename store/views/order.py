from flask import jsonify, render_template, request, make_response
from models.product_dao import Product
from flask_bootstrap import app
from maintenance.pager import Pagination
from business_logic.product_manager import list_products, list_dimensions, create_product, delete_product,\
    update_product, get_product_by_id



@app.route('/api/order', methods=['GET'])
def order():
    order_list = Product.listFilterBuyProducts((request.args.get('name')), (request.args.get('start_price')),
                                         (request.args.get('end_price')))
    order_arr = []
    for i in order_list:
        order_arr.append({'id': i.id, 'name': i.name, 'price': i.price, 'description': i.description})
    return make_response(jsonify(order=order_arr), 200)


@app.route('/api/order/<int:id>', methods=['DELETE'])
def order_id_delete(id):
    delete_product(id)
    resp = make_response(jsonify({'message': 'success'}), 200)
    return resp


@app.route('/api/order', methods=['POST'])
def order_post():
    js = request.get_json()
    create_product(js['name'], js['description'], js['price'], js['id'])
    resp = make_response('', 201)
    return resp


@app.route('/order')
def order_grid():
    return render_template('order.html')
