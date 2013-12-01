from models.product_dao import Product
from models.order_dao import Order,OrderProduct, order_product_grid
from business_logic.product_manager import validate_quantity
from flask import session
from models import Base, db_session

def product_order_update(dict):
    order_id=int(dict['order_id'])
    amount=0
    get_order = Order.get_order(order_id)
    quantity_dict = order_product_grid(session['user_id'])
    comment=dict['comment']
    delivery_type=int(dict['delivery_type'])
    delivery_address=dict['delivery_address']

    for i in quantity_dict:
        dimension_id=i.OrderProduct.dimension.id
        product_id=i.Product.id
        quantity=i.OrderProduct.quantity
        price = i.Product.price
        amount= amount + price*quantity
        total_price = price*quantity

        order_product= OrderProduct.get_order_product(order_id,product_id,dimension_id)
        order_product.quantity=quantity
        order_product.total_price=total_price
        validate_quantity(product_id,dimension_id,quantity,'update')

    get_order.status_id = 1
    get_order.delivery_id = delivery_type
    get_order.total_price = amount
    get_order.delivery_address = delivery_address
    get_order.comment = comment
    db_session.commit()

