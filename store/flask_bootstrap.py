from flask import Flask
from business_logic.validation import ValidationException ,NotFoundException
from flask import jsonify, make_response


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.from_object('config')

@app.errorhandler(ValidationException)
def val_ex(e):
    error_dict = {'message': e.message}
    return make_response(jsonify(error_dict), 400)

@app.errorhandler(NotFoundException)
def not_ex(e):
    error_dict = {'message': e.message}
    return make_response(jsonify(error_dict), 404)