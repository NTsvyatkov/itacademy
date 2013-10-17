from copy import name
from flask import render_template, flash, redirect, request
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
