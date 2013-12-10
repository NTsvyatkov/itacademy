from flask import jsonify, render_template, request, make_response, session, json
from models.user_dao import UserDao
from business_logic.order_product import product_order_update
from flask_bootstrap import app
from business_logic.product_manager import validate_quantity
from models.order_dao import order_product_grid, OrderProduct, DeliveryType
from business_logic.order_manager import update_order_details
from models.order_dao import Order
import calendar
import time

@app.route('/order_product')
def order_grid():
    assingee_list = UserDao.getUserByRole(2)
    assingee_arr = []
    for i in assingee_list:
        assingee_arr.append({'id': i.id, 'name': i.login})
    if 'user_id' in session:
        order_product = order_product_grid(session['user_id'])
    if order_product:
        return render_template('order.html',assingee_arr=assingee_arr)
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
    total_items=0
    order_date=str(order_list[0].Order.date)
    mysql_time_struct = time.strptime(order_date, '%Y-%m-%d')
    order_date = calendar.timegm(mysql_time_struct)
    if order_list[0].Order.delivery_date:
        delivery_date=str(order_list[0].Order.delivery_date)
        mysql_time_struct = time.strptime(order_date, '%Y-%m-%d')
        delivery_date = calendar.timegm(mysql_time_struct)
    else:
        delivery_date=0
    for j in quantity_list:
        dimen = j.OrderProduct.dimension.number
        total_price=total_price + j.Product.price*j.OrderProduct.quantity*dimen
        total_items=total_items+j.OrderProduct.quantity*dimen
    for i in order_list:
        order_arr.append({'order_id':i.Order.id, 'id': i.Product.id, 'name': i.Product.name, 'price': str(i.Product.price),\
         'order_status':i.Order.status.name,'description': i.Product.description,'quantity':i.OrderProduct.quantity,\
         'order_number':i.Order.order_number,'dimension':i.OrderProduct.dimension.name,'dimension_id':i.OrderProduct.dimension.id,\
         'dimension_number':i.OrderProduct.dimension.number})
    return make_response(jsonify(order=order_arr,records_amount=count, total_items=total_items,\
                delivery_date=delivery_date,\
                order_date=order_date, records_per_page=records_per_page, total_price=str(total_price)), 200)


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

@app.route('/api/order_details/', methods=['GET'])
def list_orders_id():
    records_per_page = int(request.args.get('table_size'))
    page = int(request.args.get('page'))
    order_id = int(request.args.get('order_id'))
    all_in_order, count = OrderProduct.get_by_order_product(order_id, page, records_per_page)
    quantity_of_items = OrderProduct.get_items_quantity(order_id)
    customer_name = str(all_in_order[0].order.user.first_name) + " " + \
        str(all_in_order[0].order.user.last_name + " " + "(" + str(all_in_order[0].order.user.login) + ")")
    products = []
    for i in all_in_order:
        products.append({'product_id': i.product_id, 'product_name': i.product.name,
                        'product_description': i.product.description, 'product_dimension': i.dimension.name,
                        'product_quantity': i.quantity, 'product_price': str(i.product.price)})
    order = {'customer_name': customer_name,
             'customer_type': all_in_order[0].order.user.level.name if all_in_order[0].order.user.level.name
             else "Standart",
             'order_id': all_in_order[0].order_id, 'total_price': str(all_in_order[0].order.total_price),
             'quantity_of_items': quantity_of_items,
             'assignee': str(all_in_order[0].order.assignee.first_name) + " " +
                         str(all_in_order[0].order.assignee.last_name) +
                         "(" + str(all_in_order[0].order.assignee.login) +
                         ")" if all_in_order[0].order.assignee else None,
             'order_date': str(all_in_order[0].order.date),
             'preferable_delivery_date': str(all_in_order[0].order.preferable_delivery_date),
             'order_status': all_in_order[0].order.status.name,
             'delivery_date': str(all_in_order[0].order.delivery_date),
             'gift': all_in_order[0].order.gift,
             'products': products, 'session_role': session["role"]}
    return make_response(jsonify(orders=order, all_items=count,
                                 items_per_page=records_per_page), 200)

@app.route('/api/order_details/', methods=['PUT'])
def v_update_order_details():
    js = request.json
    id = js.get('id')
    gift = True if js.get('gift') else False
    status = "Delivered" if js.get('status') else "Ordered"
    delivery_date = js.get('delivery_date')
    update_order_details(id, gift, status, delivery_date)
    if status == "Delivered":
        Order.set_user_level(id)
    return make_response(jsonify({'message': 'success'}), 200)