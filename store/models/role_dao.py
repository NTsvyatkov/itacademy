#!/usr/bin/env python
__author__ = 'andrey'

from sqlalchemy import Column, Integer, Text, String
from flask import session
from models import Base

class Role(Base):
    __tablename__ = "role"

    #role_id = Column(Integer, primary_key=True, foreign_key=ForeignKey(Action_point_to_role.role_id))
    role_id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(50))

    #role = relationship(Action_point_to_role, backref=backref('Role', lazy='dynamic'))

    def __init__(self, role_id, name):
        self.role_id = role_id
        self.name = name

    def __str__(self):
        return "CData '%s, %s'" % (self.role_id, self.name)


class RoleDao(object):

    def __init__(self, role_id, name):
        self.role_id = role_id
        self.name = name

    @staticmethod
    def getRoleByID(role_id):
        return session.query(Role).get(role_id)

    @staticmethod
    def getAllRoles():
        return session.query(Role).order_by(Role.role_id)

    def createNewRole(self):
        session.add(self)

    def updateRole(self):
        session.commit()

    @staticmethod
    def deleteRecord(roleId):
        remove_role = session.query(Role).get(roleId)
        session.delete(remove_role)
        session.commit()


