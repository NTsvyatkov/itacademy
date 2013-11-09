#!/usr/bin/env python
from sqlalchemy import and_
from flask import render_template, request, make_response, jsonify
from business_logic.product_manager import list_products
from maintenance.pager import Pagination
from views import app
from models.product_dao import Product


#@app.route('/buygrid')
#def buy_product():
#    return render_template('products_buy.html')


@app.route('/buy', methods = ['GET'])
def buy():
    list = list_products()
    array=[]
    for i in list:
        array.append({'id':i.id,'name':i.name,'price':i.price, 'description':i.description})
    return make_response(jsonify(products=array),200)


@app.route('/buygrid', methods = ['POST'])
def filterBuyProduct():
    if request.form['name'] and request.form['start_prise'] and request.form['end_prise']:
        list = Product.query.filter(and_(Product.price.between(request.form['start_prise'],request.form['end_prise'])),
                                    Product.name == request.form['name'])
    elif request.form['name']:
        list = Product.query.filter(Product.name == request.form['name'])
    elif request.form['start_prise']:
        list = Product.query.filter(Product.price.between(request.form['start_prise'],'1000000'))
    elif request.form['end_prise']:
        list = Product.query.filter(Product.price.between('0',request.form['end_prise']))
    else:
        list = list_products()
    array = []
    for i in list:
        array.append({'id':i.id,'name':i.name,'price':i.price, 'description':i.description})
    return make_response(jsonify(products=array),200)
    #return make_response(render_template('products_buy.html'),jsonify(products=array),200)



@app.route('/buygrid')
@app.route('/buygrid/<int:page>')
def buyProducts(page=1):
    all_rec = list_products()
    pagination = Pagination(5, all_rec, page)
    products = pagination.pager()
    return render_template('products_buy.html', products=products, pagination=pagination)
    #return render_template('products_buy.html')