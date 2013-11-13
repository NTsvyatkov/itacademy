__author__ = 'alex'
from flask import jsonify, render_template, request, make_response
from models.product_dao import Product
from flask_bootstrap import app
from maintenance.pager import Pagination
from business_logic.product_manager import list_products, list_dimensions, create_product, delete_product, update_product, get_product_by_id


@app.route('/CreateProduct.html', methods=('GET', 'POST'))
def CreateProduct():
        return render_template('CreateProduct.html',)

@app.route('/product_grid.html', methods=('GET', 'POST'))
def product_grid():
        return render_template('product_grid.html',)

@app.route('/product_buy.html', methods=('GET', 'POST'))
def product_buy():
        return render_template('product_buy.html',)

@app.route('/product', methods = ['GET'])
def products():
    products_list = list_products()
    products_arr=[]
    for i in products_list:
        products_arr.append({'id':i.id,'name':i.name,'price':i.price, 'description':i.description,'dimension':i.dimension.name})
    return make_response(jsonify(products=products_arr),200)

@app.route('/dimension', methods = ['GET'])
def dimensions():
    dimensions_list = list_dimensions()
    dimensions_arr=[]
    for i in dimensions_list:
        dimensions_arr.append({'id':i.id,'name':i.name})
    return make_response(jsonify(dimensions=dimensions_arr),200)


@app.route('/product/<int:id>', methods=['GET'])
def products_id(id):
    i=get_product_by_id(request.get['id'])
    product ={'id': i.id, 'name': i.name, 'price': i.price, 'description': i.description, 'dimension': i.dimension}
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


#@app.route('/productgrid')
#def productgrid():
#   return render_template('product_grid.html')

@app.route('/productgrid')
@app.route('/productgrid/<int:page>')
def productgrid(page=1):
    all_rec = Product.get_all_products()
    pagination = Pagination(5, all_rec, page)
    products = pagination.pager()
    return render_template('product_grid.html', products=products, pagination=pagination)


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