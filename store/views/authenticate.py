#!/usr/bin/env python
from flask import render_template, request, session, escape
from models.user_dao import UserDao
from views import app


@app.route('/')

@app.route('/login')
def login():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    else:
        error = 'You are not logged in'
        return render_template('login(2).html', error=error)


@app.route('/', methods=['POST', 'GET'])
@app.route('/login', methods=['POST', 'GET'])
def login_authenticate():
    if request.method == 'POST':
        if UserDao.isUserExists(request.form['name'], request.form['password']):
            session['username'] = request.form['name']
            return render_template('index.html')
        else:
            error = 'Invalid username/password'
            return render_template('login(2).html', error=error)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return render_template('login(2).html')