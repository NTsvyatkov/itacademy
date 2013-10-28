#!/usr/bin/env python
from flask import Flask, make_response, jsonify, request
from business_logic.action_point_to_role_manager import *
from business_logic.validation import ValidationException

app = Flask(__name__)

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
    action_point_to_role = {"id":ap_to_role.ap_to_role_id,"id_role": ap_to_role.role_id, "id_ap": ap_to_role.action_point_id}
    if action_point_to_role is not None:
        response = make_response(jsonify(action_point_to_role=action_point_to_role), 200)
    else:
        response = make_response(404)
    return response


@app.route('/action_point_to_role', methods=['POST'])
def createActionPointToRole():
    js = request.get_json()
    if not validationActionPointToRoleID(js('id')): #
        createActionPointToRole(js['role_id'], js['action_point_id'])
        response = make_response(201)
    else:
        response = make_response(400)
    return response


@app.route('/action_point_to_role/<int:id>', methods=['POST'])
def deleteActionPointToRole(id):
    if deleteActionPointToRole(request.get['id']):          #deleteActionPointToRole(js['id']) == True
        response = make_response(200)
    else:
        response = make_response(404)
    return response


@app.route('/action_point_to_role/<id>', methods=['PUT'])
def updateActionPointToRole():
    js = request.get_json()
    if not getActionPointToRoleByID(js['id']):
        response = make_response(404)
    elif updateActionPointToRole(js['role_id'], js['action_point_id']):
        response = make_response(200)
    else:
        response = make_response(400)
    return response


@app.errorhandler(ValidationException)
def error_handler(ex):
    error_dict = {'message': ex.message}
    return make_response(jsonify(error_dict), 404)
