#!/bin/python
from flask import render_template
from views import app
@app.route('/')
@app.route('/product_grid')
def product_grid():
    return render_template('product_grid.html')

@app.route('/search_user')
def search_user():
    return render_template('search_user.html')

@app.route('/CreateUser')
def CreateUser():
    return render_template('CreateUser.html')

@app.route('/CreateProduct')
def CreateProduct():
    return render_template('CreateProduct.html')

app.run(debug = True)

