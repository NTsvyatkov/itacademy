#!/usr/bin/env python
from flask import render_template, request
from models.user_dao import UserDao
from views import app



@app.route('/login')
def login():
    return render_template('login(2).html')

@app.route('/login', methods=['POST', 'GET'])
def login_authenticate():
    if request.method == 'POST':
        if UserDao.isUserExists(request.form['name'],request.form['password']):
            return render_template('index.html')
        else:
            return render_template('login(2).html')



