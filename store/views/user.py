from views import app
from store.maintenance.pager import Pagination
from flask import Flask, jsonify, render_template, request, make_response
from store.models.user_dao import UserDao
from store.models import db_session
from store.flask_bootstrap import app
from store.business_logic.user_manager import getListUser, getUserByID, deleteUser, createUser, updateUser
from store.business_logic.validation import ValidationException


@app.route('/create_user.html', methods=('GET', 'POST'))
def create_user():
        return render_template('create_user.html',)

@app.route('/usergrid')
def usergrid():
        return render_template('search_user.html',)


@app.route('/user', methods = ['GET'])
def users():
    user_list = getListUser()
    users_arr=[]
    for i in user_list:
        users_arr.append({'id':i.id,'login':i.login,'first_name':i.first_name, 'last_name':i.last_name,
                          'email':i.email, 'role_id':i.role_id, 'region_id':i.region_id})
    return make_response(jsonify(users=users_arr),200)


@app.route('/user/<int:id>', methods = ['GET'])
def users_id(id):
    i=getUserByID(request.get['id'])
    user ={'id':i.id,'login':i.login,'first_name':i.first_name, 'last_name':i.last_name,'email':i.email, 'role_id':i.role_id}
    resp = make_response(jsonify(users=user),200)
    return resp

@app.route('/user/<int:id>', methods=['DELETE'])
def users_id_delete(id):
    deleteUser(id)
    resp = make_response(jsonify({'message':'success'}),200)
    return resp


@app.route('/user', methods = ['POST'])
def users_post():
    js = request.get_json()
    createUser(js['user_id'],js['login'],js['first_name'],js['last_name'],js['password'],js['email'],js['region_id'],js['role_id'])
    resp = make_response(0,201)
    return resp

@app.route('/user', methods = ['PUT'])
def users_update():
    js = request.get_json()
    updateUser(js['user_id'],js['login'],js['first_name'],js['last_name'],js['password'],js['email'],js['region_id'],js['role_id'])
    resp = make_response(0,200)
    return resp

@app.errorhandler(ValidationException)
def err_han(e):
    error_dict = {'message': e.message}
    return make_response(jsonify(error_dict), 404)

@app.route('/user_grid')
@app.route('/user_grid/<int:page>')
def user_grid(page=1):
    all_rec = UserDao.get_all_products()
    pagination = Pagination(5, all_rec, page)
    user = pagination.pager()
    return render_template('layout.html', user=user, pagination=pagination)
