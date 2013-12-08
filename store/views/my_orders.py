#!/usr/bin/env python
from flask import render_template, request, make_response, jsonify, session
from flask_bootstrap import app
from models.order_dao import Order,  OrderStatus
from models.role_dao import RoleDao
from models.user_dao import UserDao


@app.route('/orders')
def my_orders():
  if session['role'] not in 'Customer':
    return "You've got permission to access this page."
  else:
    return render_template('my_orders.html',)


@app.route('/api/orders/', methods=['GET'])
def ordersPage():
    user_id = session['user_id']
    filter = ({'name': request.args.get('name_input'),
                   'order_option': request.args.get('order_option'),
                   'status_option': request.args.get('status_option')})
    records_per_page = int(request.args.get('table_size'))
    page = int(request.args.get('page'))

    prods, records_amount = Order.pagerByFilter(user_id, page, records_per_page, filter)
    orders_list = []
    for i in prods:
        orders_list.append({'order_id': i.id, 'delivery_date': i.date.strftime("%d/%m/%y"),
                            'orderStatus': OrderStatus.get_status(i.status_id).name,'total_price': str(i.total_price),
                            'assignee':UserDao.getUserByID(i.assignee_id).first_name+' '
                                       +UserDao.getUserByID(i.assignee_id).last_name,'maxDiscount': '0',
                            'role': RoleDao.getRoleByID(UserDao.getUserByID(i.assignee_id).id).name})
    return make_response(jsonify(orders=orders_list, records_amount=records_amount,
                                 records_per_page=records_per_page), 200)

@app.route('/api/orders/<int:id>', methods=['DELETE'])
def deleteOrder(id):
    Order.deleteOrder(id)
    resp = make_response(jsonify({'message': 'success'}), 200)
    return resp