#!/usr/bin/env python

from sqlalchemy import Column, Integer
from models import Base, db_session


class ActionPointToRoleDao(Base):
    __tablename__ = "action_point_to_role"

    ap_to_role_id = Column(Integer, primary_key=True, autoincrement=True)
    role_id = Column(Integer)
    action_point_id = Column(Integer)

    def __init__(self, role_id, action_point_id):
        self.role_id = role_id
        self.action_point_id = action_point_id


    def __str__(self):
        return "CData '%s, %s'" % (self.role_id, self.action_point_id)


    @staticmethod
    def getActionPointToRoleByID(apToRole_id):
        return ActionPointToRoleDao.query.get(apToRole_id).first()

    @staticmethod
    def getAllActionPointsToRole():
        return ActionPointToRoleDao.query.order_by(ActionPointToRoleDao.ap_to_role_id)

    @staticmethod
    def createNewActionPointToRole(ap_to_role_id, role_id, action_point_id):
        ap_to_role = ActionPointToRoleDao(ap_to_role_id, role_id, action_point_id)
        db_session.add(ap_to_role)
        db_session.commit()

    @staticmethod
    def updateActionPointToRole(ap_to_role_id, new_role_id, new_action_point_id):
        entry = ActionPointToRoleDao.get(ap_to_role_id)
        entry.role_id = new_role_id
        entry.action_point = new_action_point_id
        db_session.commit()

    @staticmethod
    def deleteActionPointToRole(apToRoleId):
        remove_apToRole = db_session.query(ActionPointToRoleDao).get(apToRoleId)
        db_session.delete(remove_apToRole)
        db_session.commit()
