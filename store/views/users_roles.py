#!/usr/bin/env python
from flask import make_response, jsonify, request
from store.business_logic.role_manager import getlistRole, getRoleByID, createNewRole, deleteRole, updateRole, validationRoleName
from store.business_logic.validation import ValidationException, NotFoundException


from store.flask_bootstrap import app


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
    return make_response(jsonify(roles=roles), 200)


@app.route('/roles', methods=['POST'])
def createRole():
    createNewRole(request.get_json(['id']), request.get_json(['name']))
    return make_response(201)


@app.route('/roles/<int:id>', methods=['DELETE'])
def deleteRole(id):
    deleteRole(id)
    return make_response(jsonify({'message':'success'}), 200)


@app.route('/roles', methods=['PUT'])
def updateRole():
    updateRole(request.get_json(['id']), request.get_json(['name']))
    return make_response(200)



@app.errorhandler(ValidationException)
def error_handler(ex):
    error_dict = {'message': ex.message}
    return make_response(jsonify(error_dict), 400)

@app.errorhandler(NotFoundException)
def error_handler(ex):
    error_dict = {'message': ex.message}
    return make_response(jsonify(error_dict), 404)

