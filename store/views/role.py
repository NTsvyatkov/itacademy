from flask import jsonify, render_template, request, make_response

from flask_bootstrap import app
from business_logic.role_manager import getlistRole
from business_logic.validation import ValidationException

@app.route('/api/roles', methods = ['GET'])
def roles():
    roles_list = getlistRole()
    roles_arr=[]
    for i in roles_list:
        roles_arr.append({'role_id':i.role_id,'name':i.name})
    return make_response(jsonify(roles=roles_arr), 200)
