#!/bin/python
from store.maintenance.pager import Pagination
from store.models.product_dao import Product
from flask import render_template
from views import app

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login1')
def login1():
    return render_template('login.html')

@app.route('/login_2_')
def login_2_():
    return render_template('login_2_.html')

@app.route('/product_grid')
def product_grid():
    return render_template('product_grid.html')

@app.route('/search_user')
def search_user():
    return render_template('search_user.html')

@app.route('/products_buy')
def products_buy():
    return render_template('products_buy.html')

@app.route('/CreateUser')
def CreateUser():
    return render_template('create_user.html')

@app.route('/CreateProduct')
def CreateProduct():
    return render_template('CreateProduct.html')



app.run(debug = True)

