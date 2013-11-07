from store.models.product_dao import Product, Dimension
from validation import ValidationException, NotFoundException


def validate_name(name):
    if name is None:
        raise ValidationException("Product name is required field")
    elif len(name) > 100:
        raise ValidationException("Product name length should be no more than 100 characters")


def validate_price(price):
    if price is None:
        raise ValidationException("Price is required field")
    elif not isinstance(price, float):
        raise ValidationException("Price has invalid decimal value")
    elif price < 0:
        raise ValidationException("Price can't be a negative number")


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


def list_products():
    p_list = Product.get_all_products()
    return p_list


def get_product_by_id(id):
    validate_product_id(id)
    product_by_id = Product.get_product(id)
    return product_by_id


def create_product(name, description, price, id):
    validate_name(name)
    validate_price(price)
    validate_dimension_id(id)
    Product.add_product(name, description, price, id)


def update_product(id, new_name, new_description, new_price, new_dimension):
    validate_product_id(id)
    validate_name(new_name)
    validate_price(new_price)
    validate_dimension_id(new_dimension)
    Product.upd_product(id, new_name, new_description, new_price, new_dimension)


def delete_product(id):
    validate_product_id(id)
    Product.del_product(id)


def list_dimensions():
        d_list = Dimension.get_all_dimensions()
        return d_list
