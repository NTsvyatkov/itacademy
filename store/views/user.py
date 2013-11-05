
from views import app
from flask import render_template

@app.route('/create_user.html', methods=('GET', 'POST'))
def create_user():

        return render_template('create_user.html',)