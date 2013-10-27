#!/usr/bin/env python
from flask import Flask, make_response, jsonify, request
from business_logic.action_point_manager import *
from business_logic.validation import ValidationException

app = Flask(__name__)

@app.route('/action_point', methods=['GET'])
def actionPointList():
    action_point = getListActionPoint()
    action_point_list = []
    for i in action_point:
        action_point_list.append({i.action_point_id, i.action_point_name})
    return make_response(jsonify(action_point_list=action_point_list), 200)


@app.route('/action_point/<id>', methods=['GET'])
def actionPointByID():
    js = request.get_json()
    ap_id = getActionPointByID(js['id'])
    action_point = {ap_id.action_point_id, ap_id.action_point_name}
    if action_point is not None:
        response = make_response(jsonify(action_point=action_point), 200)
    else:
        response = make_response(404)
    return response


@app.route('/action_point', methods=['POST'])
def createActionPoint():
    js = request.get_json()
    if validationActionPointName(js('name')):
        createActionPoint(js['id'], js['name'])
        response = make_response(201)
    else:
        response = make_response(400)
    return response


@app.route('/action_point/<id>', methods=['POST'])
def deleteActionPoint():
    js = request.get_json()
    if deleteActionPoint(js['id']):          #deleteActionPoint(js['id']) == True
        response = make_response(200)
    else:
        response = make_response(404)
    return response


@app.route('/action_point/<id>', methods=['PUT'])
def updateActionPoint():
    js = request.get_json()
    if not getActionPointByID(js['id']):
        response = make_response(404)
    elif updateActionPoint(js['id'], js['name']):
        response = make_response(200)
    else:
        response = make_response(400)
    return response


@app.errorhandler(ValidationException)
def error_handler(ex):
    error_dict = {'message': ex.message}
    return make_response(jsonify(error_dict), 404)
