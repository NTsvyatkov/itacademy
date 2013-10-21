#!/usr/bin/env python
__author__ = 'andrey'

from sqlalchemy import Column, Integer
from flask import session
from models import Base


class Action_point_to_role(Base):
    __tablename__ = "action_point_to_role"

    ap_to_role_id = Column(Integer, primary_key=True)
    role_id = Column(Integer)
    action_point_id = Column(Integer)

    def __init__(self, ap_to_role_id, role_id, action_point_id):
        self.ap_to_role_id = ap_to_role_id
        self.role_id = role_id
        self.action_point_id = action_point_id


    def __str__(self):
        return "CData '%s, %s, %s'" % (self.ap_to_role_id, self.role_id, self.action_point_id)


class ActionPointToRoleDao(object):

    def __init__(self, ap_to_role_id, role_id, action_point_id):
        self.ap_to_role_id = ap_to_role_id
        self.role_id = role_id
        self.action_point_id = action_point_id

    @staticmethod
    def getActionPointToRoleByID(apToRole_id):
        return [session.query(Action_point_to_role).get(apToRole_id).first()]

    @staticmethod
    def getAllActionPointsToRole():
        return session.query(Action_point_to_role).order_by(Action_point_to_role.ap_to_role_id)

    def createNewActionPointToRole(self):
        session.add(self)

    def updateActionPointToRole(self):
        session.commit()

    @staticmethod
    def deleteActionPointToRole(apToRoleId):
        remove_apToRole = session.query(Action_point_to_role).get(apToRoleId)
        session.delete(remove_apToRole)
        session.commit()
