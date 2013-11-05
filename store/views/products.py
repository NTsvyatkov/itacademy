__author__ = 'alex'
from flask import jsonify, render_template, request, make_response
from models.product_dao import Product
from models import db_session
from flask_bootstrap import app
from business_logic.product_manager import list_products, create_product, delete_product, update_product, get_product_by_id
from business_logic.validation import ValidationException

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

#@app.route('/productgrid')
#def productgrid():
#   return render_template('product_grid.html')

@app.route('/productgrid')
@app.route('/productgrid/<int:page>')
def productgrid(page=1):
    products = db_session.query(Product).order_by(Product.name).slice(start=1, stop=2).all()
    return render_template('product_grid.html', products = products)

#@app.route('/productgrid')
#def productgrid():
#    if 'username' in db_session:
#        return render_template('product_grid.html')
#    else:
#        error = 'You are not logged in'
#        return render_template('login(2).html', error=error)

#p=db_session.query(Product).order_by(Product.name).slice(start=0, stop=4).all()
#for i in p:
#    print i