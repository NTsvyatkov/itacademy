from flask import jsonify, render_template, request, make_response
from models.product_dao import Dimension
from flask_bootstrap import app
from maintenance.pager import Pagination
from business_logic.product_dimension_manager import list_dimension, create_dimension, delete_dimension, update_dimension, get_dimension_by_id
from business_logic.validation import ValidationException


@app.route('/api/products/dimensions', methods = ['GET'])
def dimension():
    dimension_list = list_dimension()
    dimension_arr=[]
    for i in dimensions_list:
        dimension_arr.append({'id':i.id,'dimension':i.dimension.name})
    return make_response(jsonify(dimension=dimension_arr),200)

@app.route('/api/products/dimensions/<int:id>', methods=['GET'])
def dimensions_id(id):
    i=get_dimension_by_id(request.get['id'])
    dimensions ={'id': i.id, 'dimension': i.dimension.name}
    resp = make_response(jsonify(dimensions=dimensions),200)
    return resp

@app.route('/api/products/dimensions', methods = ['POST'])
def dimensions_post():
    js = request.get_json()
    create_dimension(js['dimension'],js['id'])
    resp = make_response(0,201)
    return resp


@app.route('/api/products/dimensions/<int:id>', methods=['DELETE'])
def dimensions_id_delete(id):
    delete_dimension(id)
    resp = make_response(jsonify({'message':'success'}),200)
    return resp


@app.route('/api/products/dimensions', methods = ['PUT'])
def dimension_update():
    js = request.get_json()
    update_dimension(js['id'],js['dimensions'])
    resp = make_response(0,200)
    return resp


@app.errorhandler(ValidationException)
def err_han(e):
    error_dict = {'message': e.message}
    return make_response(jsonify(error_dict), 404)


@app.route('/productgrid')
@app.route('/productgrid/<int:page>')
def productgrid(page=1):
    all_rec = dimension.get_all_dimensions()
    pagination = Pagination(5, all_rec, page)
    dimensions = pagination.pager()
    return render_template('product_grid.html', dimensions=dimensions, pagination=pagination)
