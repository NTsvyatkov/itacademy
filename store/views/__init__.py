from flask_bootstrap import app
from views import views_app
from views import products
from models import session
from views import authenticate

@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()