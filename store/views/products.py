from flask import jsonify, render_template, request, make_response, redirect, url_for
from models.product_dao import Product, Dimension
from flask_bootstrap import app
from business_logic.product_manager import list_products, list_dimensions, create_product, delete_product,\
    update_product, get_product_by_id, validate_quantity
from models.product_stock_dao import ProductStock


@app.route('/create_product', methods=('GET', 'POST'))
def CreateProduct():
        return render_template('create_product.html',)


@app.route('/product_grid', methods=('GET', 'POST'))
def product_grid():
        return render_template('product_grid.html',)



@app.route('/api/dimension', methods=['GET'])
def dimensions():
    dimensions_list = list_dimensions()
    dimensions_arr = []
    for i in dimensions_list:
        dimensions_arr.append({'id': i.id, 'name': i.name})
    return make_response(jsonify(dimensions=dimensions_arr), 200)


@app.route('/api/products/', methods=['GET'])
def products_page():
    records_per_page = int(request.args.get('table_size'))
    page = int(request.args.get('page'))
    filter_dict = {'name': request.args.get('name'),
                   'name_options': request.args.get('name_options'),
                   'description': request.args.get('description'),
                   'description_options': request.args.get('description_options'),
                   'price': request.args.get('price'),
                   'price_options': request.args.get('price_options')}
    all_rec, count = Product.filter_product_grid(filter_dict, page, records_per_page)
    products_arr = []
    for i in all_rec:
        products_arr.append({'id': i.id, 'name': i.name, 'price': str(i.price), 'description': i.description,
                             })
    return make_response(jsonify(products=products_arr, records_amount=count,
                                 records_per_page=records_per_page), 200)


@app.route('/api/product/<int:id>', methods=['GET'])
def products_id(id):
    i = get_product_by_id(request.get['id'])
    product = {'id': i.id, 'name': i.name, 'price': str(i.price), 'description': i.description, 'dimension': i.dimension}
    resp = make_response(jsonify(products=product), 200)
    return resp


@app.route('/api/product/<int:id>', methods=['DELETE'])
def products_id_delete(id):
    delete_product(id)
    resp = make_response(jsonify({'message': 'success'}), 200)
    return resp


@app.route('/api/product', methods=['POST'])
def products_post():
    js = request.get_json()
    create_product(js['name'], js['description'], js['price'], js['id'])
    resp = make_response('', 201)
    return resp

@app.route('/api/product_', methods=['POST'])
def products_post_():
    js = request.get_json()
    create_product(js['name'], js['description'], js['price'])
    resp = make_response('', 201)
    return resp


@app.route('/api/product', methods=['PUT'])
def products_update():
    js = request.get_json()
    update_product(js['id'], js['name'], js['description'], js['price'])
    return make_response(jsonify({'message':'success'}),200)

@app.route('/product_edit')
def product_edit():
    return render_template('product_edit.html')

@app.route('/product_edit/<int:id>')
def productsId(id):
    print(id)
    return redirect(url_for('product_edit'))

@app.route('/api/product_stock', methods=['GET', 'POST'])
def stockList():
    productStock = ProductStock.getStockByProduct(1)
    productStockList = []
    for i in productStock:
        productStockList.append({'dimension': Dimension.get_dimension(i.dimension_id).name, 'quantity': i.quantity,
                                 'dimension_id': i.dimension_id})
    product = ({"name": Product.get_product(1).name, "description": Product.get_product(1).description,
                "price": str(Product.get_product(1).price)})
    return make_response(jsonify(productStock=productStockList, product=product), 200)


@app.route('/api/stock', methods=['PUT'])
def updateStock():
    js = request.get_json()
    ProductStock.updateProductStock(js['product_id'], js['dimension_id'], js['quantity'])
    return make_response(jsonify({'message':'success'}),200)
