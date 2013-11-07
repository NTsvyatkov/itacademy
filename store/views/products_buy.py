#!/usr/bin/env python
from flask import render_template, request, make_response, jsonify
from business_logic.product_manager import list_products
from views import app


@app.route('/buygrid')
def buy_product():
    return render_template('products_buy.html')


@app.route('/buy', methods = ['GET'])
def buy():
    list = list_products()
    array=[]
    for i in list:
        array.append({'id':i.id,'name':i.name,'price':i.price, 'description':i.description})
    return make_response(jsonify(products=array),200)

#
#@app.route('/buy', methods = ['POST'])
#def filterBuyProduct():
#    list = Product.query.filter_by(and_(name == request.form['name'], prise between request.form['start_prise'] and request.form['end_prise']))
#    for i in list:
#        array.append({'id':i.id,'name':i.name,'price':i.price, 'description':i.description})
#    return make_response(jsonify(products=array),200)
