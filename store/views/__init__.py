#from flask import Flask
#app = Flask(__name__, template_folder='../templates', static_folder='../static')
#app.config.from_object('config')
#import views.user



from flask_bootstrap import app
from views import views_app, user
from views import products
from models import db_session
from views import authenticate
