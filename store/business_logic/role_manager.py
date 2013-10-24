#!/usr/bin/env python

from models.role_dao import RoleDao
from validation import ValidationException


def validationRoleID(role_id):
    if not RoleDao.getRoleByID(role_id):
        raise ValidationException("Unable to find role with given id")
    else:
        return True


def validationRoleName(role_name):
    if role_name is None:
        raise ValidationException("The role name is required field")
    elif len(role_name) > 50:
        raise ValidationException("Name length should be no more than 50 characters")
    else:
        return True


def getlistRole():
    return RoleDao.getAllRoles()


def createNewRole(role_id, name):
    validationRoleName(name)
    RoleDao.createNewRole()


def updateRole(role_id, name):
    validationRoleID(role_id)
    validationRoleName(name)
    RoleDao.updateRole()


def deleteRole(role_id):
    validationRoleID(role_id)
    RoleDao.deleteRecord(role_id)



def getRoleByID(role_id):
    validationRoleID(role_id)
    return RoleDao.getRoleByID(role_id)




