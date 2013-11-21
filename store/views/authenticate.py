#!/usr/bin/env python
from flask import render_template, request, session, escape
from models.user_dao import UserDao
from models.role_dao import RoleDao
from flask_bootstrap import app


@app.route('/')

@app.route('/login')
def login():
    if 'login' in session:
        return 'Logged in as %s' % escape(session['login'])
    else:
        error = 'You are not logged in'
        return render_template('login(2).html', error=error)


@app.route('/', methods=['POST', 'GET'])
@app.route('/login', methods=['POST', 'GET'])
def login_authenticate():
    if request.method == 'POST':
        if UserDao.isUserExists(request.form['name'], request.form['password']):
            user = UserDao.getUserByLogin(request.form['name'], request.form['password'])
            session['login'] = user.login
            #session['id'] = user.id
            #session['role'] = RoleDao.getRoleByID(user.role_id).name
            return render_template('index.html')
        else:
            error = 'Invalid username/password'
            return render_template('login(2).html', error=error)

@app.route('/logout')
def logout():
    session.pop('login', None)
    #session.pop('id', None)
    #session.pop('role', None)
    return render_template('login(2).html')