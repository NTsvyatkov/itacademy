from flask import jsonify, render_template, request, make_response

from flask_bootstrap import app
from models.region_dao import RegionDao
from maintenance.pager_region import Pagination
from business_logic.region_manager import getlistRegion, createRegion, updateRegion, deleteRegion, getRegionByID, getlistRegion
from business_logic.validation import ValidationException

@app.route('/region', methods=('GET', 'POST', 'PUT'))
def region():
        return render_template('region.html',)

@app.route('/api/regions', methods = ['GET'])
def regions():
    regions_list = getlistRegion()
    regions_arr=[]
    for i in regions_list:
        regions_arr.append({'region_id':i.region_id,'name':i.name})
    return make_response(jsonify(regions=regions_arr), 200)


@app.route('/api/regions/<int:id>', methods=['GET'])
def regions_id(id):
    i=getRegionByID(request.base_url.get['id'])
    region ={'region_id': i.region_id, 'name': i.name}
    resp = make_response(jsonify(regions=region), 200)
    return resp

@app.route('/api/regions/<int:page>', methods=['GET'])
def region_page(page):
    all_rec = RegionDao.getlistRegion()
    records_per_page = 5
    pagination = Pagination(records_per_page, all_rec, page)
    prods = pagination.pager()
    records_amount = len(all_rec)
    regions_arr = []
    for i in prods:
        regions_arr.append({'name': i.name})
    return make_response(jsonify(regions=regions_arr, records_amount=records_amount,
                                 records_per_page=records_per_page), 200)


@app.route('/api/regions', methods = ['POST'])
def regions_post():
    js = request.get_json()
    createRegion(js['name'])
    resp = make_response('', 201)
    return resp


@app.route('/api/regions/<int:id>', methods=['DELETE'])
def regions_id_delete(id):
    deleteRegion(id)
    resp = make_response(jsonify({'message':'success'}), 200)
    return resp


@app.route('/api/regions', methods = ['PUT'])
def regions_update():
    js = request.json
    updateRegion(js['region_id'],js['name'])
    resp = make_response('0', 200)
    return resp


@app.errorhandler(ValidationException)
def err_han(e):
    error_dict = {'message': e.message}
    return make_response(jsonify(error_dict), 400)



@app.errorhandler(ValidationException)
def err_han(e):
    error_dict = {'message': e.message}
    return make_response(jsonify(error_dict), 404)
