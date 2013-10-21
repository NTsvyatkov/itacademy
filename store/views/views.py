from copy import name
from flask import Flask, jsonify, render_template, flash, redirect, request, make_response
app = Flask(__name__)
#from app import app
#from forms import LoginForm
from wtforms import form
import sys
sys.path.append('../business_logic')
from product import list_products, get_product_id, create_product
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



app.route('/productgrid')
def productgrid():
    return render_template('product_grid.html')
