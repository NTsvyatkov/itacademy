#!/usr/bin/env python
from flask import render_template, request, session, escape, redirect, url_for
from models.user_dao import UserDao
from models.role_dao import RoleDao
from flask_bootstrap import app


@app.route('/')

@app.route('/login')
def login():
    if 'login' in session:
        return render_template('layout.html')
    else:
        error = 'You are not logged in'
        return render_template('login(2).html', error=error)


@app.route('/', methods=['POST'])
@app.route('/login', methods=['POST'])
def login_authenticate():
    if UserDao.isUserExists(request.form['name'], request.form['password']):
        user = UserDao.getUserByLogin(request.form['name'], request.form['password'])
        session['login'] = user.login
        session['user_id'] = user.id
        session['role'] = RoleDao.getRoleByID(user.role_id).name
        return render_template('layout.html')
    else:
        error = 'Invalid username/password'
        return render_template('login(2).html', error=error)

@app.route('/logout')
def logout():
    session.pop('login', None)
    session.pop('id', None)
    session.pop('role', None)
    return redirect(url_for('login'))
