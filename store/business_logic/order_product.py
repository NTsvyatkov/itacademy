from models.product_dao import Product
from models.order_dao import Order,OrderProduct, order_product_grid
from business_logic.product_manager import validate_quantity
from business_logic.product_manager import get_product_by_id
from flask import session
from models import Base, db_session
import datetime

def product_order_update(order_dict,method):
    order_id=int(order_dict['order_id'])
    amount=0
    order = Order.get_order(order_id)
    quantity_dict=order_dict['product_quantity']
    if order_dict.get('assignee'):
        assignee=int(order_dict['assignee'])
    else:
         assignee=None
    if (order_dict['preferable_delivery_date']):
        preferable_delivery_date=int(order_dict['preferable_delivery_date'])/1000
        preferable_delivery_date=(datetime.datetime.fromtimestamp(preferable_delivery_date).strftime('%Y-%m-%d'))
    else:
        preferable_delivery_date=0
    for i in quantity_dict:
        dimension_id=i['dimension_id']
        product_id=i['product_id']
        quantity=i['quantity']
        validate_quantity(product_id,dimension_id,quantity,'update')
        dimension_number=i['dimension_number']
        get_product=get_product_by_id(product_id)
        price = get_product.price
        amount= amount + price*quantity*dimension_number
        order_product= OrderProduct.get_order_product(order_id,product_id,dimension_id)
        if order_product:
            order_product.quantity=quantity
        else:
            order_product= OrderProduct.add_order_product(order_id,product_id,dimension_id,quantity,price)
        OrderProduct.changeTriggerStatus(order_dict['order_id'],i['product_id'],i['dimension_id'])

    if method == 'POST':
        order.status_id = 3
    else:
        order.status_id = 4
    order.total_price = amount
    order.assignee_id = assignee
    order.preferable_delivery_date=preferable_delivery_date
    db_session.commit()

