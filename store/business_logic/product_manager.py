from models.product_dao import Product, Dimension
from models.product_stock_dao import ProductStock
from validation import ValidationException, NotFoundException
import re

def validate_name(name):
    if name is None:
        raise ValidationException("Product name is required field")
    elif len(name) > 100:
        raise ValidationException("Product name length should be no more than 100 characters")


def validate_price(price):
    if price is None:
        raise ValidationException("Price is required field")
    elif not re.match("^\d+(?:\.\d{0,2})?$", str(price)):
        raise ValidationException("Price has invalid decimal value")
    elif float(price) <= 0:
        raise ValidationException("Price should be a positive number")


def validate_product_id(id):
    if id is None:
        raise ValidationException("Product id is required field")
    if not Product.get_product(id):
        raise NotFoundException("Unable to find product with given id")


def validate_dimension_id(id):
    if id is None:
        raise ValidationException("Dimension is required field")
    if not Dimension.get_dimension(id):
        raise NotFoundException("Unable to find dimension with given id")

def validate_quantity(product_id,dimension_id,quantity,check):
    if not ProductStock.get_quantity_result(product_id,dimension_id,quantity,check):
        raise ValidationException("Sorry, there are no such quantity = "+str(quantity)+" with this dimension id="
                                    +str(dimension_id)+" and product id = "+str(product_id)+" in the stock.")

def list_products():
    p_list = Product.get_all_products()
    return p_list


def get_product_by_id(id):
    validate_product_id(id)
    product_by_id = Product.get_product(id)
    return product_by_id


def create_product(name, description, price):
    validate_name(name)
    validate_price(price)
    Product.add_product(name, description, price)


def update_product(id, new_name, new_description, new_price):
    validate_product_id(id)
    validate_name(new_name)
    validate_price(new_price)
    Product.upd_product(id, new_name, new_description, new_price)


def delete_product(id):
    validate_product_id(id)
    Product.del_product(id)


def list_dimensions():
        d_list = Dimension.get_all_dimensions()
        return d_list
