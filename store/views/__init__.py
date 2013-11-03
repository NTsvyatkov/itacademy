from flask import Flask
app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config.from_object('config')
from views import views_app
from views import products
from models import session
from views import authenticate

@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()