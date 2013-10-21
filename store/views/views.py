from copy import name
from flask import Flask, jsonify, render_template, flash, redirect, request
from app import app
from forms import LoginForm
from wtforms import form



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
  
//Products views
@app.route('/products', methods = ['GET', 'POST'])
def products():

    a = request.form["name"]
    b = request.form["name"]
    products = [{"id":"1", "name":"apple", "description":"Sweet apple", "price":"10.5", "dimension":"kg"},
                {"id":"2", "name":a, "description":"Sweet aorange", "price":"15.4", "dimension":"kg"},
                {"id":"3", "name":"Banana", "description":"Sweet banana", "price":"25.4", "dimension":"kg"}
                ]
    return jsonify(products=products)


@app.route('/productgrid')
def productgrid():
    return render_template('product_grid.html')
//end products views