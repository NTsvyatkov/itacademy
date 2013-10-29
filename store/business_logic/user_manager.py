#!/usr/bin/env python
__author__ = 'andrey'

import re
from validation import ValidationException
from models.region_dao import RegionDao
from models.role_dao import RoleDao
from models.user_dao import UserDao


def validationLogin(login):
    if login is None:
        raise ValidationException("Login is required field")
    elif len(login) > 50:
        raise ValidationException("Login length should be no more than 50 characters")
    elif not re.match("^[a-zA-Z0-9]*_?[a-zA-Z0-9]*$", str(login)):
        raise ValidationException("Login should contain only alphanumerical characters.")


def validationFirstName(first_name):
    if first_name is None:
        raise ValidationException("First Name is required field")
    elif len(first_name) > 50:
        raise ValidationException("First Name length should be no more than 50 characters")


def validationLastName(last_name):
    if last_name is None:
        raise ValidationException("Last Name is required field")
    elif len(last_name) > 50:
        raise ValidationException("Last Name length should be no more than 50 characters")


def validationPassword(password):
    if password is None:
        raise ValidationException("Password is required field")
    elif len(password) > 20:
        raise ValidationException("Password length should be no more than 50 characters")


def validationEmail(email):
    if email is None:
        raise ValidationException("Email is required field")
    elif len(email) > 100:
        raise ValidationException("Email length should be no more than 50 characters")
    elif not re.match("[\w\.\-]*@[\w\.\-]*\.\w+", str(email)):
        raise ValidationException("Invalid email field")



def validationRoleID(role_id):
    if role_id is None:
        raise ValidationException("Role is required field")
    elif not isinstance(role_id, int):
        raise ValidationException("Role has invalid integer value")
    elif not RoleDao.getRoleByID(role_id):
        raise ValidationException("Unable to find user role with given id")


def validationRegionID(region_id):
    if region_id is None:
        raise ValidationException("Region is required field")
    elif not isinstance(region_id, int):
        raise ValidationException("Role has invalid integer value")
    elif not RegionDao.getRegionByID(region_id):
        raise ValidationException("Unable to find a region with given id")


def validationUserID(user_id):
    if not UserDao.getUserByID(user_id):
        raise ValidationException("Unable to find  user with given id")


def getListUser():
    return UserDao.getAllUsers()

def createUser(user_id, login, first_name, last_name, password, email, region_id, role_id):
    validationLogin(login)
    validationFirstName(first_name)
    validationLastName(last_name)
    validationPassword(password)
    validationEmail(email)
    validationRegionID(region_id)
    validationRoleID(role_id)
    UserDao.createNewUser()


def updateUser(user_id, login, first_name, last_name, password, email, region_id, role_id):
    validationUserID(user_id)
    validationLogin(login)
    validationFirstName(first_name)
    validationLastName(last_name)
    validationPassword(password)
    validationEmail(email)
    validationRegionID(region_id)
    validationRoleID(role_id)

    UserDao.updateUser()


def deleteUser(user_id):
    validationUserID(user_id)
    UserDao.deleteRecord(user_id)


def getUserByID(user_id):
    validationUserID(user_id)
    return UserDao.getUserByID(user_id)








