#!/usr/bin/env python
from flask import make_response, jsonify, request
from business_logic.action_point_manager import *
from business_logic.validation import ValidationException

from flask_bootstrap import app

@app.route('/action_point', methods=['GET'])
def actionPointList():
    action_point = getListActionPoint()
    action_point_list = []
    for i in action_point:
        action_point_list.append({"id": i.action_point_id, "name": i.action_point_name})
    return make_response(jsonify(action_point_list=action_point_list), 200)


@app.route('/action_point/<int:id>', methods=['GET'])
def actionPointByID(id):
    ap_id = getActionPointByID(request.get['id'])
    action_point = {"id": ap_id.action_point_id, "name": ap_id.action_point_name}
    return make_response(jsonify(action_point=action_point), 200)


@app.route('/action_point', methods=['POST'])
def createActionPoint():
    js = request.get_json()
    createActionPoint(js['id'], js['name'])
    return make_response(201)


@app.route('/action_point/<int:id>', methods=['POST'])
def deleteActionPoint(id):
    deleteActionPoint(id)
    return make_response(jsonify({'message':'success'}),200)


@app.route('/action_point', methods=['PUT'])
def updateActionPoint():
    js = request.get_json()
    updateActionPoint(js['id'], js['name'])
    return make_response(200)


@app.errorhandler(ValidationException)
def error_handler(ex):
    error_dict = {'message': ex.message}
    return make_response(jsonify(error_dict), 404)
