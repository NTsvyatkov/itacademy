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


@app.route('/api/buy/<name>/<start_prise>/<end_prise>', methods = ['POST'])
def filterBuyProducts(name, start_prise, end_prise):

    #if request.form['name'] and request.form['start_prise'] and request.form['end_prise']:
    #    list = Product.query.filter(and_(Product.price.between(request.form['start_prise'],request.form['end_prise'])),
    #                                Product.name == request.form['name'])
    #elif request.form['name']:
    #    list = Product.query.filter(Product.name == request.form['name'])
    #elif request.form['start_prise']:
    #    list = Product.query.filter(Product.price.between(request.form['start_prise'],'1000000'))
    #elif request.form['end_prise']:
    #    list = Product.query.filter(Product.price.between('0',request.form['end_prise']))
    #else:
    #    list = list_products()
    #array = []
    #for i in list:
    #    array.append({'id':i.id,'name':i.name,'price':i.price, 'description':i.description})
    #return make_response(jsonify(products=array),200)

    #query = Product.query
    #if request.form['name']:
    #    list = qu.filter(Product.name == request.query_string.get('name'))
    #if request.form['start_prise']:
    #    list = qu.filter(Product.price.between('0',request.form['end_prise']))
    #if request.form['end_prise']:
    #    list = qu.filter(Product.price.between('0',request.form['end_prise']))
    #else:
    #    list = list_products()


    #list = filterByStartPrise(start_prise)

    #list = filterByEndPrise(end_prise)

    list = filterByProductName(name)

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