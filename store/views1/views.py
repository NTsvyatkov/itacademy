from copy import name
from flask import Flask, jsonify, render_template, flash, redirect, request, make_response, send_from_directory
from views1 import app
#zfrom forms import LoginForm
from wtforms import form
from business_logic.product import list_products, create_product,delete_product,update_product,get_product_by_id
from business_logic.validation import ValidationException

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
        products_arr.append({'id':i.id,'name':i.name,'price':i.price, 'description':i.description,'dimension':i.dimension.name})

    return make_response(jsonify(products=products_arr),200)


@app.route('/product/<int:id>', methods = ['GET'])
def products_id(id):
    i=get_product_by_id(request.get['id'])
    product ={'id':i.id,'name':i.name,'price':i.price, 'description':i.description,'dimension':i.description}
    resp = make_response(jsonify(products=product),200)
    return resp

@app.route('/product/<int:id>', methods=['DELETE'])
def products_id_delete(id):
    delete_product(id)
    resp = make_response(jsonify({'message':'success'}),200)
    return resp


@app.route('/product', methods = ['POST'])
def products_post():
    js = request.get_json()
    create_product(js['name'],js['description'],js['price'],js['id'])
    resp = make_response(0,201)
    return resp

@app.route('/product', methods = ['PUT'])
def products_update():
    js = request.get_json()
    update_product(js['id'],js['name'],js['description'],js['price'],js['dim_id'])
    resp = make_response(0,200)
    return resp

@app.errorhandler(ValidationException)
def err_han(e):
    error_dict = {'message': e.message}
    return make_response(jsonify(error_dict), 404)

@app.route('/static/<path:filename>')
def send_file(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/productgrid')
def productgrid():
    return render_template('product_grid.html')
