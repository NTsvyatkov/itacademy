#!/usr/bin/env python

from models.action_point_to_role_dao import ActionPointToRoleDao
from validation import ValidationException


def validationActionPointToRoleID(ap_to_role_id):
    if not ActionPointToRoleDao.getActionPointToRoleByID(ap_to_role_id):
        raise ValidationException("Unable to find role action point with given id")
    else:
        return True


def validationActionPointToRoleName(ap_to_role_name):
    if ap_to_role_name is None:
        raise ValidationException("The role action point name is required field")
    elif len(ap_to_role_name) > 50:
        raise ValidationException("Name length should be no more than 50 characters")
    else:
        return True


def getlistActionPointToRole():
    return ActionPointToRoleDao.getAllActionPointsToRole()


def createActionPointToRole(ap_to_role_id, name):
    validationActionPointToRoleName(name)
    ActionPointToRoleDao.createNewActionPointToRole()


def updateActionPointToRole(ap_to_role_id, name):
    validationActionPointToRoleID(ap_to_role_id)
    validationActionPointToRoleName(name)
    ActionPointToRoleDao.createNewActionPointToRole()


def deleteActionPointToRole(ap_to_role_id):
    validationActionPointToRoleID(ap_to_role_id)
    ActionPointToRoleDao.deleteActionPointToRole(ap_to_role_id)



def getActionPointToRoleByID(ap_to_role_id):
    validationActionPointToRoleID(ap_to_role_id)
    return ActionPointToRoleDao.getActionPointToRoleByID(ap_to_role_id)




