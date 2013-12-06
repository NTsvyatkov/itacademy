from flask import jsonify, render_template, request, make_response, session, json
from models.order_dao import OrderProduct
from business_logic.order_product import product_order_update
from flask_bootstrap import app
from business_logic.product_manager import validate_quantity
from models.order_dao import order_product_grid, OrderProduct, DeliveryType


@app.route('/order_product')
def order_grid():
    delivery_list = DeliveryType.get_delivery_all()
    delivery_arr = []
    for i in delivery_list:
        delivery_arr.append({'id': i.id, 'name': i.name})
    if 'user_id' in session:
        order_product = order_product_grid(session['user_id'])
    if order_product:
        return render_template('order.html',delivery_arr=delivery_arr)
    else:
        return render_template('order_empty.html')


@app.route('/api/order_product/', methods=['GET'])
def order():
    records_per_page = int(request.args.get('table_size'))
    page = int(request.args.get('page'))
    order_arr = []
    if 'user_id' in session:
        order_list,count = order_product_grid(session['user_id'],page, records_per_page)
        quantity_list = order_product_grid(session['user_id'])
    else:
        order_list,count = order_product_grid(4,page, records_per_page)
        quantity_list = order_product_grid(4)
    total_price=0
    for j in quantity_list:
        dimen = j.OrderProduct.dimension.number
        total_price=total_price + j.Product.price*j.OrderProduct.quantity*dimen
    for i in order_list:
        order_arr.append({'order_id':i.Order.id, 'id': i.Product.id, 'name': i.Product.name, 'price': str(i.Product.price),\
         'description': i.Product.description,'quantity':i.OrderProduct.quantity,\
         'dimension':i.OrderProduct.dimension.name,'dimension_id':i.OrderProduct.dimension.id,\
         'dimension_number':i.OrderProduct.dimension.number})
    return make_response(jsonify(order=order_arr,records_amount=count,\
                                 records_per_page=records_per_page, total_price=str(total_price)), 200)


@app.route('/api/order_product/<int:id_product>/<int:id_order>/<int:dimension_id>', methods=['DELETE'])
def order_id_delete(id_order,id_product,dimension_id):
    OrderProduct.delete_order_product(id_order,id_product,dimension_id)
    resp = make_response(jsonify({'message': 'success'}), 200)
    return resp


@app.route('/api/order_product/', methods=['PUT'])
def order_post():
    js = request.json
    product_order_update(js)
    resp = make_response(jsonify({'message': 'success'}), 200)
    return resp

@app.route('/api/update/', methods=['PUT'])
def quantity_post():
    js = request.json
    validate_quantity(js['product_id'],js['dimension_id'],js['quantity'],'check');
    OrderProduct.update_order_product(js['order_id'],js['product_id'],js['dimension_id'], js['quantity'],js['price'])
    resp = make_response(jsonify({'message': 'success'}), 200)
    return resp

@app.route('/order/<int:id>', methods=['GET'])
def order_details(id):
    return render_template('order_details.html')

@app.route('/api/orders/<int:id>', methods=['GET'])
def list_orders_id(id):
    all_in_order = OrderProduct.get_by_product(id)
    quantity_of_items = OrderProduct.get_items_quantity(id)
    products = []
    for i in all_in_order:
        products.append({'product_id': i.product_id, 'product_name': i.product.name,
                        'product_description': i.product.description, 'product_quantity': i.quantity,
                        'product_dimension': i.dimension.name, 'product_price': str(i.product.price)})

# 'user_name': all_in_order[0].order.user.login
# 'assignee': all_in_order[0].order.assignee.login if all_in_order[0].order.assignee else None,
# 'delivery_date': str(all_in_order[0].order.delivery_date),
# 'gift': all_in_order[0].order.gift,
    order = {'order_id': all_in_order[0].order_id,
             'date': str(all_in_order[0].order.date), 'order_status': all_in_order[0].order.status.name,
             'delivery': all_in_order[0].order.delivery.name, 'total_price': str(all_in_order[0].order.total_price),
             'preferable_delivery_date': str(all_in_order[0].order.preferable_delivery_date),
             'delivery_address': all_in_order[0].order.delivery_address, 'quantity_of_items': quantity_of_items,
             'comments': all_in_order[0].order.comment, 'products': products, 'session_role': session["role"]}
    if session["role"] == "Customer":
        order['gift'] = all_in_order[0].order.gift
        order['delivery_date'] = str(all_in_order[0].order.delivery_date)
    elif session["role"] == "Supervisor":
        order['assignee'] = all_in_order[0].order.assignee.login if all_in_order[0].order.assignee else None
        order['user_name'] = all_in_order[0].order.user.login
        order['delivery_date'] = str(all_in_order[0].order.delivery_date)
        order['gift'] = all_in_order[0].order.gift
    return make_response(jsonify(orders=order), 200)

