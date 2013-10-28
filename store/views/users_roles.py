#!/usr/bin/env python
from flask import Flask, make_response, jsonify, request
from business_logic.role_manager import getlistRole, getRoleByID, createNewRole, deleteRole, updateRole, validationRoleName
from business_logic.validation import ValidationException


app = Flask(__name__)


@app.route('/roles', methods=['GET'])
def rolesList():
    roles = getlistRole()
    roles_list = []
    for i in roles:
        roles_list.append({"id": i.role_id, "name": i.name})
    return make_response(jsonify(roles=roles_list), 200)


@app.route('/roles/<int:id>', methods=['GET'])
def rolesByID(id):
    role = getRoleByID(request.get['id'])
    roles = {"id": role.role_id, "name": role.name}
    if roles is not None:
        response = make_response(jsonify(roles=roles), 200)
    else:
        response = make_response(404)
    return response


@app.route('/roles', methods=['POST'])
def createRole():
    js = request.get_json()
    if validationRoleName(js('name')):
        createNewRole(js['id'], js['name'])
        response = make_response(201)
    else:
        response = make_response(400)
    return response


@app.route('/roles/<int:id>', methods=['POST'])
def deleteRole(id):
    if deleteRole(id):
        response = make_response(200)
    else:
        response = make_response(404)
    return response


@app.route('/roles/<id>', methods=['PUT'])
def updateRole():
    js = request.get_json()
    if not getRoleByID(js['id']):
        response = make_response(404)
    elif updateRole(js['id'], js['name']):
        response = make_response(200)
    else:
        response = make_response(400)
    return response


@app.errorhandler(ValidationException)
def error_handler(ex):
    error_dict = {'message': ex.message}
    return make_response(jsonify(error_dict), 404)
