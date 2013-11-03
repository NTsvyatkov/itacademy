#!/usr/bin/env python
__author__ = 'andrey'

from sqlalchemy import Column, Integer
from models import Base, session


class ActionPointToRoleDao(Base):
    __tablename__ = "action_point_to_role"

    ap_to_role_id = Column(Integer, primary_key=True, autoincrement=True)
    role_id = Column(Integer)
    action_point_id = Column(Integer)

    def __init__(self, ap_to_role_id, role_id, action_point_id):
        self.ap_to_role_id = ap_to_role_id
        self.role_id = role_id
        self.action_point_id = action_point_id


    def __str__(self):
        return "CData '%s, %s, %s'" % (self.ap_to_role_id, self.role_id, self.action_point_id)


    @staticmethod
    def getActionPointToRoleByID(apToRole_id):
        return [session.query(ActionPointToRoleDao).get(apToRole_id).first()]

    @staticmethod
    def getAllActionPointsToRole():
        return session.query(ActionPointToRoleDao).order_by(ActionPointToRoleDao.ap_to_role_id)

    @staticmethod
    def createNewActionPointToRole(ap_to_role_id, role_id, action_point_id):
        ap_to_role = ActionPointToRoleDao(ap_to_role_id, role_id, action_point_id)
        session.add(ap_to_role)
        session.commit()

    @staticmethod
    def updateActionPointToRole(ap_to_role_id, new_role_id, new_action_point_id):
        entry = ActionPointToRoleDao.get(ap_to_role_id)
        entry.role_id = new_role_id
        entry.action_point = new_action_point_id
        session.commit()

    @staticmethod
    def deleteActionPointToRole(apToRoleId):
        remove_apToRole = session.query(ActionPointToRoleDao).get(apToRoleId)
        session.delete(remove_apToRole)
        session.commit()
