#!/usr/bin/env python

from sqlalchemy import Column, Integer, Text, String, ForeignKey
from action_point_to_role_dao import ActionPointToRoleDao
from sqlalchemy.orm import relationship, backref
from models import Base, db_session


class RoleDao(Base):
    __tablename__ = "role"

    role_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))

    def __init__(self,name):
        super(RoleDao, self).__init__()
        self.name = name

    def __str__(self):
        return "CData '%s'" % (self.name)


    @staticmethod
    def getRoleByID(role_id):
        return RoleDao.query.get(role_id)

    @staticmethod
    def getAllRoles():
        return RoleDao.query.order_by(RoleDao.role_id)

    @staticmethod
    def createNewRole(name):
        role = RoleDao(name)
        db_session.add(role)
        db_session.commit()

    @staticmethod
    def updateRole(id, new_name):
        entry = RoleDao.get(id)
        entry.name = new_name
        db_session.commit()

    @staticmethod
    def deleteRecord(roleId):
        remove_role = db_session.query(RoleDao).get(roleId)
        db_session.delete(remove_role)
        db_session.commit()

    @staticmethod
    def get_assignee_all():
        return RoleDao.query.all()


