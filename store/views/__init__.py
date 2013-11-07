from flask import Flask
app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config.from_object('config')
import views.user



from store.flask_bootstrap import app
from store.models import db_session
from views import  products_buy
