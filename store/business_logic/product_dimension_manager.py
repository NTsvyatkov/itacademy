from models.product_dao import  Dimension
from validation import ValidationException, NotFoundException

def validate_name(name):
    if name is None:
        raise ValidationException("name is required field")
    elif len(name) > 100:
        raise ValidationException("name length should be no more than 100 characters")


def validate_dimension_id(id):
    if id is None:
        raise ValidationException("Dimension is required field")
    if not Dimension.get_dimension(id):
        raise NotFoundException("Unable to find dimension with given id")

def list_dimension():
    d_list = Dimension.get_all_dimensions()
    return d_list


def get_dimension_by_id(id):
    validate_dimension_id(id)
    dimension_by_id = Dimension.get_dimension(id)
    return dimension_by_id


def create_dimension(name, id):
    validate_name(name)
    validate_dimension_id(id)
    Dimension.add_dimension(name, id)


def update_dimension(id, new_name):
    validate_dimension_id(id)
    validate_name(new_name)
    Dimension.upd_dimension(id, new_name)


def delete_dimension(id):
    validate_dimension_id(id)
    Dimension.del_dimension(id)


def list_dimensions():
        d_list = Dimension.get_all_dimensions()
        return d_list
