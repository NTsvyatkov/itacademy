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
    for i in dimension_list:
        dimension_arr.append({'id':i.id,'dimension':i.name})
    return make_response(jsonify(dimension=dimension_arr),200)

@app.route('/api/products/dimensions/<int:id>', methods=['GET'])
def dimension_id(id):
    i=get_dimension_by_id(request.get['id'])
    dimension ={'id': i.id, 'dimension': i.name}
    resp = make_response(jsonify(dimension=dimension),200)
    return resp

@app.route('/api/products/dimensions', methods = ['POST'])
def dimension_post():
    js = request.get_json()
    create_dimension(js['dimensions'],js['id'])
    resp = make_response(0,201)
    return resp


@app.route('/api/products/dimensions/<int:id>', methods=['DELETE'])
def dimension_id_delete(id):
    delete_dimension(id)
    resp = make_response(jsonify({'message':'success'}),200)
    return resp


@app.route('/api/products/dimensions', methods = ['PUT'])
def dimension_update():
    js = request.get_json()
    update_dimension(js['id'],js['dimension'])
    resp = make_response(0,200)
    return resp

