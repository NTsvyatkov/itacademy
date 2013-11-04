#!/usr/bin/env python

from business_logic.action_point_manager import validationActionPointID
from business_logic.role_manager import validationRoleID
from models.action_point_to_role_dao import ActionPointToRoleDao
from validation import ValidationException, NotFoundException


def validationActionPointToRoleID(ap_to_role_id):
    if not ActionPointToRoleDao.getActionPointToRoleByID(ap_to_role_id):
        raise NotFoundException("Unable to find role action point with given id")
    else:
        return True



def getlistActionPointToRole():
    return ActionPointToRoleDao.getAllActionPointsToRole()


def createActionPointToRole(ap_to_role_id, role_id, action_point):
    validationRoleID(role_id)
    validationActionPointID(action_point)
    ActionPointToRoleDao.createNewActionPointToRole(ap_to_role_id, role_id, action_point)


def updateActionPointToRole(ap_to_role_id, role_id, action_point):
    validationActionPointToRoleID(ap_to_role_id)
    validationRoleID(role_id)
    validationActionPointID(action_point)
    ActionPointToRoleDao.createNewActionPointToRole(ap_to_role_id, role_id, action_point)


def deleteActionPointToRole(ap_to_role_id):
    validationActionPointToRoleID(ap_to_role_id)
    ActionPointToRoleDao.deleteActionPointToRole(ap_to_role_id)



def getActionPointToRoleByID(ap_to_role_id):
    validationActionPointToRoleID(ap_to_role_id)
    return ActionPointToRoleDao.getActionPointToRoleByID(ap_to_role_id)




