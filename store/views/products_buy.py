#!/usr/bin/env python
from sqlalchemy import and_
from flask import render_template, request, make_response, jsonify
from business_logic.product_manager import list_products, filterByStartPrise, filterByEndPrise, filterByProductName
from maintenance.pager import Pagination
from flask_bootstrap import app
from models.product_dao import Product


@app.route('/api/buy', methods = ['GET'])
def listBuyProducts():
    list = list_products()
    array=[]
    for i in list:
        array.append({'id':i.id,'name':i.name,'price':i.price, 'description':i.description})
    return make_response(jsonify(products=array),200)


@app.route('/api/buy/<int:id>/<int:value>', methods = ['POST'])
def amountProducts(id, value):
    print(id)
    print(value)
    return make_response(jsonify({'message':'success'}),200)


@app.route('/api/buy', methods = ['POST'])
def filterBuyProducts():

    if request.json['name']:
        list = filterByProductName(request.json['name'])
    if request.json['start_prise']:
        list = filterByStartPrise(request.json['start_prise'])
    if request.json['end_prise']:
        list = filterByEndPrise(request.json['end_prise'])
    array = []
    for i in list:
        array.append({'id':i.id,'name':i.name,'price':i.price, 'description':i.description})
    return make_response(jsonify(products=array),200)



#@app.route('/buygrid')
#@app.route('/buygrid/<int:page>')
#def buyProducts(page=1):
#    all_rec = list_products()
#    pagination = Pagination(5, all_rec, page)
#    products = pagination.pager()
#    return render_template('product_buy.html', products=products, pagination=pagination)
#