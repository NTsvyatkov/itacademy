from flask_bootstrap import app
from views import views_app
from views import products
from models import session

@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()