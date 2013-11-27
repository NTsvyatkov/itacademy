from flask import render_template, request, make_response, jsonify, session
from flask_bootstrap import app
from maintenance.pager_order import Pagination
from business_logic.order_manager import getListOrder, get_order_by_id, list_status, list_delivery, list_assignee, update_orders
from models.order_dao import Order, OrderProduct, OrderStatus, DeliveryType




@app.route('/current_orders', methods=('GET', 'POST'))
def current_orders():
        return render_template('current_order2.html',)

@app.route('/api/status', methods=['GET'])
def status():
    status_list = list_status()
    status_arr = []
    for i in status_list:
        status_arr.append({'id': i.id, 'name': i.name})
    return make_response(jsonify(status=status_arr), 200)

@app.route('/api/assignee', methods=['GET'])
def assignee():
    assignee_list = Order.query
    assignee_arr = []
    for i in assignee_list:
        assignee_arr.append({'id': i.assignee_id, 'assignee_id': i.assignee.role.name})
    return make_response(jsonify(assignee=assignee_arr), 200)


@app.route('/api/delivery', methods=['GET']) 
def delivery():
    delivery_list = list_delivery()
    delivery_arr = []
    for i in delivery_list:
        delivery_arr.append({'id': i.id, 'name': i.name})
    return make_response(jsonify(delivery=delivery_arr), 200)

#@app.route('/api/order', methods=['GET'])
#def orders():
#    orders_list = getListOrder()
#    orders_arr = []
#    for i in orders_list:
#        orders_arr.append({'id': i.id, 'user_id': i.user.last_name, 'status_id': i.status.name})
#    return make_response(jsonify(orders=orders_arr), 200)


#@app.route('/api/order/<int:page>', methods=['GET'])
#def orders_page(page):
#    all_rec = Order.getAllOrders()
#    records_per_page = 5
#    pagination = Pagination(records_per_page, all_rec, page)
#    prods = pagination.pager()
#    records_amount = len(all_rec)
#    orders_arr = []
#    for i in prods:
#        orders_arr.append({'id': i.id, 'user_id': (i.user.first_name + " " + i.user.last_name), 'status_id': i.status.name, 'amount': '0.00' })
#    return make_response(jsonify(orders=orders_arr, records_amount=records_amount,
#                                 records_per_page=records_per_page), 200)
#@app.route('/api/order2/<int:page>', methods=['GET'])
#def orders_page2(page):
#    all_rec = Order.getAllOrders()
#    records_per_page = 10
#    pagination = Pagination(records_per_page, all_rec, page)
#    prods = pagination.pager()
#    records_amount = len(all_rec)
#    orders_arr = []
#    for i in prods:
#        orders_arr.append({'id': i.id, 'user_id': (i.user.first_name + " " + i.user.last_name), 'status_id': i.status.name, 'amount': '0.00' })
#    return make_response(jsonify(orders=orders_arr, records_amount=records_amount,
#                                 records_per_page=records_per_page), 200)


@app.route('/api/order', methods=['GET'])
def orders():
    status_id = request.args.get('status_id')
    assignee_id = request.args.get('assignee_id')
    records_per_page = int(request.args.get('table_size'))
    page = int(request.args.get('page'))
    orders, records_amount = Order.pagerByFilterOrder(status_id, assignee_id, page, records_per_page)
    orders_arr = []
    for i in orders:
        orders_arr.append({'id': i.id, 'user_id': (i.user.first_name + " " + i.user.last_name), 'status_id': i.status.name, 'total_price': i.total_price,'assignee_id' : i.assignee.role.name})
    return make_response(jsonify(orders=orders_arr, records_amount=records_amount,
                                 records_per_page=records_per_page), 200)

@app.route('/api/order', methods = ['PUT'])
def update_order():
    js = request.json
    update_orders(js['id'], js['new_status_id'],js['new_delivery_id'],js['new_delivery_address'],js['new_comment'] )
    resp = make_response('', 200)
    return resp



@app.route('/api/order/<int:id>', methods=['GET'])
def orders_id(id):
    i = get_order_by_id(request.get['id'])
    order = {'id': i.id, 'user_id': i.user_id, 'status_id': i.status_id}
    resp = make_response(jsonify(orders=order), 200)
    return resp