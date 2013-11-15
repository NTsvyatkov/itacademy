#!/usr/bin/env python


from business_logic.user_manager import validationRoleID
from models.role_dao import RoleDao
from validation import ValidationException



def validationRoleName(role_name):
    if role_name is None:
        raise ValidationException("The role name is required field")
    elif len(role_name) > 50:
        raise ValidationException("Name length should be no more than 50 characters")


def getlistRole():
    return RoleDao.getAllRoles()


def createNewRole(name):
    validationRoleName(name)
    RoleDao.createNewRole(name)


def updateRole(role_id, name):
    validationRoleID(role_id)
    validationRoleName(name)
    RoleDao.updateRole(role_id, name)


def deleteRole(role_id):
    validationRoleID(role_id)
    RoleDao.deleteRecord(role_id)


def getRoleByID(role_id):
    validationRoleID(role_id)
    return RoleDao.getRoleByID(role_id)




