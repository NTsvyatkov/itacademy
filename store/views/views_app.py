from copy import name
from flask import jsonify, render_template, flash, redirect, request, make_response, send_from_directory
from flask_bootstrap import app
#from forms import LoginForm
from wtforms import form
from business_logic.product_manager import list_products, create_product,delete_product,update_product,get_product_by_id
from business_logic.validation import ValidationException
from models.product_dao import Product

#@app.route('/login')

#@app.route('/login', methods = ['GET', 'POST'])
#def login():
#    form = LoginForm()
#    login1 = ('12345')
#    password1 = ('12345')
#    if form.validate_on_submit():
#        if form.login == login1 and form.password == password1:
#
#            redirect('/index')
#        else:
#
#            return  ('The username or password you entered is incorrect.')
#
#    return  render_template('login.html', form=form)
  


@app.route('/static/<path:filename>')
def send_file(filename):
    return send_from_directory(app.static_folder, filename)



#@app.route('/productgrid')
#@app.route('/productgrid/<int:page>')
#def productgrid(page=1):
#    products = Product.query.order_by(Product.name.asc()).paginate(page, 2, False)
#    return render_template('product_grid.html', products = products)
