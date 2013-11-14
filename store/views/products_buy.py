#!/usr/bin/env python
from sqlalchemy import and_
from flask import render_template, request, make_response, jsonify
from business_logic.product_manager import list_products
from maintenance.pager import Pagination
from flask_bootstrap import app
from models.product_dao import Product


@app.route('/api/buy/<int:id>', methods = ['POST'])
def amountProducts(id):
    print(id)
    print(request.get_json('value'))
    return make_response(jsonify({'message':'success'}),200)


@app.route('/api/buy', methods = ['GET'])
def filterBuyProducts():
    list = Product.listFilterBuyProducts((request.args.get('name')),(request.args.get('start_price')),
                                         (request.args.get('end_price')))
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