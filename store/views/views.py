from copy import name
from flask import Flask, jsonify, render_template, flash, redirect, request, make_response, json
app = Flask(__name__)
#from app import app
#from forms import LoginForm
from wtforms import form
import sys
sys.path.append('../business_logic')
from product import list_products, get_product_id, create_product
from business_logic.validation import ValidationException

from business_logic.user_manager import getListUser, getUserByID,deleteUser,createUser,updateUser
from business_logic.validation import ValidationException
from models import User


@app.route('/login')


@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    login1 = ('12345')
    password1 = ('12345')
    if form.validate_on_submit():
        if form.login == login1 and form.password == password1:

            redirect('/index')
        else:

            return  ('The username or password you entered is incorrect.')

    return  render_template('login.html', form=form)
  
@app.route('/product', methods = ['GET'])
def products():
    products_list = list_products()
    products_arr=[]
    for i in products_list:
        products_arr.append({i.id,i.name,i.description,i.description})

    return make_response(jsonify(products=products_arr),200)

@app.route('/product/<id>', methods = ['GET'])
def products_id():
    js = request.get_json()
    product_id = get_product_id(js['id'])
    product ={product_id.id,product_id.name,product_id.description,product_id.description}
    resp = make_response(jsonify(products=product),200)
    return resp

@app.route('/product', methods = ['POST'])
def products_post():
    js = request.get_json()
    create_product(js['name'],js['description'],js['price'],js['id'])
    resp = make_response(0,200)
    return resp

@app.errorhandler(ValidationException)
def err_han(e):
    error_dict = {'message': e.message}
    return make_response(jsonify(error_dict), 404)

@app.route('/user', methods = ['GET'])
def user():
    userlist = getListUser()
    user_arr=[]
    for i in userlist:
        user_arr.append({'id':i.id,'login':i.login,'first_name':i.first_name, 'last_name':i.last_name,'email':i.email,'role_id':i.role_id,'region_id':i.region_id})
    return make_response(jsonify(user=user_arr),200)
listUser()

@app.route('/user/<id>', methods = ['GET'])
def userid():
    js = request.get_json()
    user_id = getUserByID(js['id'])
    user ={'id':i.id,'login':i.login,'first_name':i.first_name, 'last_name':i.last_name,'email':i.email,'role_id':i.role_id,'region_id':i.region_id}
    resp = make_response(jsonify(user=user),200)
    return resp

@app.route('/user', methods = ['DELETE'])
def user_id_delete():
    js = request.get_json()
    deleteUser(js['id'])
    resp = make_response(jsonify({'message':'success'}),200)
    return resp


@app.route('/user', methods = ['POST'])
def user_post():
    js = request.get_json()
    createUser(js['user_id'],js['login'],js['first_name'],js['last_name'],js['password'],js['email'],js['region_id'],js['role_id'])
    resp = make_response(0,201)
    return resp

@app.route('/user', methods = ['PUT'])
def user_update():
    js = request.get_json()
    updateUser(js['user_id'],js['login'],js['first_name'],js['last_name'],js['password'],js['email'],js['region_id'],js['role_id'])
    resp = make_response(0,200)
    return resp

@app.errorhandler(ValidationException)
def err_han(e):
    error_dict = {'message': e.message}
    return make_response(jsonify(error_dict), 404)

app.route('/productgrid')
def productgrid():
    return render_template('product_grid.html')



@app.route('/create_user', methods=('GET', 'POST'))
def create_user():

        return render_template('create_user.html',)

@app.route('/create_user_data', methods=['POST'])
def create_user_data():

    if request.method == 'POST':

        user_data = request.json
        name= user_data['name']
        first_name = user_data['first_name']
        last_name = user_data['last_name']
        password = user_data['password']
        email = user_data['email']
        region_id = user_data['region_id']
        role_id = user_data['role_id']

        return jsonify(result = name + first_name+last_name + password+email+ region_id + role_id)
