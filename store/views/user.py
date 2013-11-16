

from flask import Flask, jsonify, render_template, request, make_response
from models.user_dao import UserDao
from models import db_session
from flask_bootstrap import app
from maintenance.pager_user import Pagination
from business_logic.user_manager import getListUser, getUserByID, deleteUser, createUser, updateUser
from business_logic.validation import ValidationException, NotFoundException


@app.route('/create_user', methods=('GET', 'POST'))
def create_user():
        return render_template('create_user.html',)

@app.route('/search_user', methods=('GET', 'POST'))
def search_user():
        return render_template('search_user.html',)

@app.route('/usergrid')
def usergrid():
        return render_template('search_user.html',)


@app.route('/api/user', methods = ['GET'])
def users():
    user_list = getListUser()
    users_arr=[]
    for i in user_list:
        users_arr.append({'id':i.id,'login':i.login,'first_name':i.first_name, 'last_name':i.last_name,
                          'email':i.email, 'role_id':i.role_id, 'region_id':i.region_id})

    return make_response(jsonify(users=users_arr),200)

@app.route('/api/user/<int:page>', methods=['GET'])
def users_page(page):
    all_rec = UserDao.getAllUsers()
    records_per_page = 5
    pagination = Pagination(records_per_page, all_rec, page)
    prods = pagination.pager()
    records_amount = len(all_rec)
    users_arr = []
    for i in prods:
        users_arr.append({'login': i.login, 'first_name': i.first_name, 'last_name': i.last_name, 'role_id': i.role_id,
                             'email': i.email, 'region_id': i.region_id})
    return make_response(jsonify(users=users_arr, records_amount=records_amount,
                                 records_per_page=records_per_page), 200)


@app.route('/api/user/<int:id>', methods = ['GET'])
def users_id(id):
    i=getUserByID(id)
    user ={'id':i.id,'login':i.login,'first_name':i.first_name, 'last_name':i.last_name,'email':i.email, 'role_id':i.role_id}
    resp = make_response(jsonify(users=user),200)
    return resp

@app.route('/api/user/<int:id>', methods=['DELETE'])
def users_id_delete(user_id):
    deleteUser(user_id)
    resp = make_response(jsonify({'message':'success'}),200)
    return resp


@app.route('/api/user', methods = ['POST'])
def users_post():
    js = request.get_json()
    createUser(js['user_id'],js['login'],js['first_name'],js['last_name'],js['password'],js['email'],js['region_id'],js['role_id'])
    resp = make_response(0,201)
    return resp

@app.route('/api/user', methods = ['PUT'])
def users_update():
    js = request.get_json()
    updateUser(js['user_id'],js['login'],js['first_name'],js['last_name'],js['password'],js['email'],js['region_id'],js['role_id'])
    resp = make_response(0,200)
    return resp

@app.errorhandler(ValidationException)
def err_han(e):
    error_dict = {'message': e.message}
    return make_response(jsonify(error_dict), 400)
    
    
@app.errorhandler(NotFoundException)
def err_han(ex):
    error_dict = {'message': ex.message}
    return make_response(jsonify(error_dict), 404)


