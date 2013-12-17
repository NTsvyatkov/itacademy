from flask import render_template, request, make_response, jsonify, session
from flask_bootstrap import app
from models.order_dao import Order,  OrderStatus
from models.role_dao import RoleDao
from models.user_dao import UserDao
from operator import itemgetter


@app.route('/manage_orders')
def manage_orders():
  if session['role'] not in 'Merchandiser':
    return "You've got permission to access this page."
  else:
    return render_template('manage_orders.html',)




@app.route('/api/manage_orders/', methods=['GET'])
def page_order():
    user_id = session['user_id']
    filter = ({'name': request.args.get('name_input'),
                   'order_option': request.args.get('order_option'),
                   'status_option': request.args.get('status_option')})
    records_per_page = int(request.args.get('table_size'))
    page = int(request.args.get('page'))
    prods, records_amount = Order.pagerByFilterByMerchandiser(user_id, page, records_per_page, filter)
    orders_list = []
    for i in prods:
        orders_list.append({'order_id': i.id,'orderStatus': OrderStatus.get_status(i.status_id).name,'total_price': str(i.total_price),
                            'user':i.user.first_name+' '
                                       + i.user.last_name,
                            'role': RoleDao.getRoleByID(UserDao.getUserByID(i.assignee_id).id).name})
    return make_response(jsonify(orders=orders_list, records_amount=records_amount,
                                 records_per_page=records_per_page), 200)

