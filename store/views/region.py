from flask import jsonify, render_template, request, make_response

from flask_bootstrap import app
from business_logic.region_manager import getlistRegion, createRegion, updateRegion, deleteRegion, getRegionByID
from business_logic.validation import ValidationException

@app.route('/region.html', methods=('GET', 'POST'))
def create_user():
        return render_template('region.html',)

@app.route('/region', methods = ['GET'])
def regions():
    regions_list = getlistRegion()
    regions_arr=[]
    for i in regions_list:
        regions_arr.append({'region_id':i.region_id,'name':i.name})
    return make_response(jsonify(regions=regions_arr),200)


@app.route('/region/<int:id>', methods=['GET'])
def regions_id(id):
    i=getRegionByID(request.get['id'])
    region ={'region_id': i.region_id, 'name': i.name}
    resp = make_response(jsonify(regions=region),200)
    return resp


@app.route('/region', methods = ['POST'])
def regions_post():
    js = request.json()
    createRegion(js['region_id'],js['name'])
    resp = make_response(0,201)
    return resp


@app.route('/region/<int:id>', methods=['DELETE'])
def regions_id_delete(id):
    deleteRegion(id)
    resp = make_response(jsonify({'message':'success'}),200)
    return resp


@app.route('/region', methods = ['PUT'])
def regions_update():
    js = request.get_json()
    updateRegion(js['region_id'],js['name'])
    resp = make_response(0,200)
    return resp


@app.errorhandler(ValidationException)
def err_han(e):
    error_dict = {'message': e.message}
    return make_response(jsonify(error_dict), 400)



@app.errorhandler(ValidationException)
def err_han(e):
    error_dict = {'message': e.message}
    return make_response(jsonify(error_dict), 404)
