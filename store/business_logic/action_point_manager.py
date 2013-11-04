#!/usr/bin/env python

from models.action_point_dao import ActionPointDao
from validation import ValidationException, NotFoundException


def validationActionPointID(ap_id):
    if not ActionPointDao.getActionPointByID(ap_id):
        raise NotFoundException("Unable to find action point with given id")
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
    ActionPointDao.createNewActionPoint(ap_id, name)


def updateActionPoint(ap_id, name):
    validationActionPointID(ap_id)
    validationActionPointName(name)
    ActionPointDao.updateActionPoint(ap_id, name)


def deleteActionPoint(ap_id):
    validationActionPointID(ap_id)
    ActionPointDao.deleteActionPoint(ap_id)


def getActionPointByID(ap_id):
    validationActionPointID(ap_id)
    return ActionPointDao.getActionPointByID(ap_id)




