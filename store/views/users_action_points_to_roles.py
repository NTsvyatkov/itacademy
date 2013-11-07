#!/usr/bin/env python
from flask import make_response, jsonify, request
from store.business_logic.action_point_to_role_manager import *
from store.business_logic.validation import ValidationException

from store.flask_bootstrap import app

@app.route('/action_point_to_role', methods=['GET'])
def actionPointToRoleList():
    action_point_to_role = getlistActionPointToRole()
    ap_to_role_list = []
    for i in action_point_to_role:
        ap_to_role_list.append({"id": i.ap_to_role_id, "id_role": i.role_id, "id_ap": i.action_point_id})
    return make_response(jsonify(action_point_list=ap_to_role_list), 200)


@app.route('/action_point_to_role/<int:id>', methods=['GET'])
def actionPointToRoleByID(id):
    ap_to_role = getActionPointToRoleByID(request.get['id'])
    action_point_to_role = {"id":ap_to_role.ap_to_role_id,"role_id": ap_to_role.role_id,
                            "action_point_id": ap_to_role.action_point_id}
    return make_response(jsonify(action_point_to_role=action_point_to_role), 200)



@app.route('/action_point_to_role', methods=['POST'])
def createActionPointToRole():
    createActionPointToRole(request.get_json(['ap_to_role_id']),request.get_json(['role_id']),
                            request.get_json(['action_point_id']))
    return make_response(201)


@app.route('/action_point_to_role/<int:id>', methods=['POST'])
def deleteActionPointToRole(id):
    deleteActionPointToRole(id)
    return make_response(jsonify({'message':'success'}),200)


@app.route('/action_point_to_role', methods=['PUT'])
def updateActionPointToRole():
    updateActionPointToRole(request.get_json(['ap_to_role_id']), request.get_json(['role_id']),
                            request.get_json(['action_point_id']))
    return make_response(200)


@app.errorhandler(ValidationException)
def error_handler(ex):
    error_dict = {'message': ex.message}
    return make_response(jsonify(error_dict), 404)
