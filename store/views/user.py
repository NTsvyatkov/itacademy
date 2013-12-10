
from flask import Flask, jsonify, render_template, request, make_response
from models.user_dao import UserDao, RoleDao, RegionDao
from models import db_session
from flask_bootstrap import app
from maintenance.pager_user import Pagination
from business_logic.user_manager import getListUser, getUserByID, deleteUser, createUser, updateUser, delete_user
from business_logic.validation import ValidationException, NotFoundException
from views.authenticate import session

@app.route('/create_user', methods=('GET', 'POST'))
def create_user():
    if session['role'] not in 'Administrator':
       return "You've got permission to access this page."
    else:
        return render_template('create_user.html',)


@app.route('/edit_user', methods=('GET', 'POST'))
def edit_user():
        return render_template('edit_user.html',)


@app.route('/search_user', methods=('GET', 'POST'))
def search_user():
    if session['role'] not in 'Administrator':
       return "You've got permission to access this page."
    else:
       return render_template('search_user.html',)

@app.route('/usergrid')
def usergrid():
        return render_template('search_user.html',)

@app.route('/users_')
def users_list():
        return render_template('users.html',)



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
        users_arr.append({'id':i.id,'login': i.login, 'first_name': i.first_name, 'last_name': i.last_name,
                          'role_id': RoleDao.getRoleByID(i.role_id).name, 'email': i.email,
                          'region_id': RegionDao.getRegionByID(i.region_id).name})
    return make_response(jsonify(users=users_arr, records_amount=records_amount,
                                 records_per_page=records_per_page), 200)
@app.route('/api/users', methods=['GET'])
def user_pager():
    records_per_page = int(request.args.get('table_size'))
    page = int(request.args.get('page'))
    users, records_amount = UserDao.pagerByFilterUsers(page, records_per_page)
    users_arr = []
    for i in users:
        users_arr.append({'id':i.id,'login': i.login, 'first_name': i.first_name, 'last_name': i.last_name,
                          'role_id': RoleDao.getRoleByID(i.role_id).name, 'email': i.email,
                          'region_id': RegionDao.getRegionByID(i.region_id).name})
    return make_response(jsonify(users=users_arr, records_amount=records_amount,
                                 records_per_page=records_per_page), 200)



@app.route('/api/users/<int:id>', methods = ['GET'])
def users_id(id):
    i=getUserByID(id)
    user ={'id':i.id,'login':i.login,'first_name':i.first_name, 'last_name':i.last_name,'email':i.email,'region_id':i.region_id, 'role_id':RoleDao.getRoleByID(i.role_id).name}
    resp = make_response(jsonify(users=user),200)
    return resp

#This route don't work
#@app.route('/api/edit_user/<int:id>', methods = ['GET'])
#def users_id(id):
#    i=getUserByID(id)
#    user ={'login':i.login,'first_name':i.first_name, 'last_name':i.last_name,'email':i.email,'region_id':i.region_id, 'role_id':RoleDao.getRoleByID(i.role_id).name}
#    resp = make_response(jsonify(users=user),200)
#    return resp


@app.route('/api/user/<int:user_id>', methods=['DELETE'])
def users_id_delete(user_id):
    deleteUser(user_id)
    resp = make_response(jsonify({'message':'success'}),200)
    return resp


@app.route('/api/user', methods = ['POST'])
def users_post():
    js = request.json
    createUser(js['login'], js['password'], js['first_name'], js['last_name'], js['email'], js['region_id'],
               js['role_id'])
    resp = make_response('', 201)
    return resp

@app.route('/api/user', methods = ['PUT'])
def users_update():
    js = request.json
    updateUser(js['user_id'],js['login'],js['password'],js['first_name'],js['last_name'],js['email'],js['role_id'],js['region_id'],)
    resp = make_response('',200)
    return resp

@app.errorhandler(ValidationException)
def err_han(e):
    error_dict = {'message': e.message}
    return make_response(jsonify(error_dict), 400)
    
    
@app.errorhandler(NotFoundException)
def err_han(ex):
    error_dict = {'message': ex.message}
    return make_response(jsonify(error_dict), 404)

@app.route('/api/user_/<int:id>', methods=['DELETE'])
def users_id_delete_(id):
    delete_user(id)
    resp = make_response(jsonify({'message': 'success'}), 200)
    return resp
