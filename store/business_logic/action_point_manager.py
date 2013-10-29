#!/usr/bin/env python

from models.action_point_dao import ActionPointDao
from validation import ValidationException


def validationActionPointID(ap_id):
    if not ActionPointDao.getActionPointByID(ap_id):
        raise ValidationException("Unable to find action point with given id")
    else:
        return True


def validationActionPointName(ap_name):
    if ap_name is None:
        raise ValidationException("The action point name is required field")
    elif len(ap_name) > 50:
        raise ValidationException("Name length should be no more than 50 characters")
    else:
        return True


def getListActionPoint():
    return ActionPointDao.getAllActionPoints()


def createActionPoint(ap_id, name):
    validationActionPointName(name)
    ActionPointDao.createNewActionPoint()


def updateActionPoint(ap_id, ap_name):
    validationActionPointID(ap_id)
    validationActionPointName(ap_name)
    ActionPointDao.updateActionPoint() #!!


def deleteActionPoint(ap_id):
    validationActionPointID(ap_id)
    ActionPointDao.deleteActionPoint(ap_id)


def getActionPointByID(ap_id):
    validationActionPointID(ap_id)
    return ActionPointDao.getActionPointByID(ap_id)




