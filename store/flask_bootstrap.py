from flask import Flask
from business_logic.validation import ValidationException, NotFoundException
from flask import jsonify, make_response
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.from_object('config')
from traceback import format_exc

@app.errorhandler(ValidationException)
def err_han(e):
    error_dict = {'message': e.message}
    return make_response(jsonify(error_dict), 404)

@app.errorhandler(BaseException)
def err_han2(e):
    error_dict = {'message': 'This operation not permitted  on the server'}
    print(format_exc())
    return make_response(jsonify(error_dict), 500)

@app.errorhandler(NotFoundException)
def err_han3(e):
    error_dict = {'message': e.message}
    return make_response(jsonify(error_dict), 400)