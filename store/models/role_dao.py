#!/usr/bin/env python
__author__ = 'andrey'


from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, Text, String
from action_point_to_role_dao import ActionPointToRoleDao
from flask import session
from sqlalchemy.orm import relationship, backref
from models import Base

class RoleDao(Base):
    __tablename__ = "role"

    role_id = Column(Integer, ForeignKey('action_point_to_role.role_id'), primary_key=True, autoincrement=True) #fix foreignkey property
    name = Column(String(50))

    role = relationship(ActionPointToRoleDao, backref=backref('role', lazy='dynamic'))

    def __init__(self, role_id, name):
        self.role_id = role_id
        self.name = name

    def __str__(self):
        return "CData '%s, %s'" % (self.role_id, self.name)


    @staticmethod
    def getRoleByID(role_id):
        return session.query(RoleDao).get(role_id)

    @staticmethod
    def getAllRoles():
        return session.query(RoleDao).order_by(RoleDao.role_id)

    @staticmethod
    def createNewRole(id, name):
        role = RoleDao(id, name)
        session.add(role)
        session.commit()

    @staticmethod
    def updateRole(id, new_name):
        entry = RoleDao.get(id)
        entry.name = new_name
        session.commit()

    @staticmethod
    def deleteRecord(roleId):
        remove_role = session.query(RoleDao).get(roleId)
        session.delete(remove_role)
        session.commit()


