#!/usr/bin/env python

from action_point_to_role_dao import ActionPointToRoleDao
from models import Base, db_session, engine
from sqlalchemy import Column, Date, Integer, String, DATE, ForeignKey, Text, Float
from sqlalchemy.orm import relationship, backref


class ActionPointDao(Base):
    __tablename__ = "action_point"

    #action_point_id = Column(Integer, ForeignKey('action_point_to_role.ap_to_role_id'), primary_key=True ,
    #                         autoincrement=True)
    action_point_id = Column(Integer, primary_key=True, autoincrement=True)
    action_point_name = Column(String)

    #action_point = relationship(ActionPointToRoleDao, backref=backref('action_point', lazy='dynamic'))


    def __init__(self, action_point_name):
        super(ActionPointDao, self).__init__()
        self.action_point_name = action_point_name


    def __str__(self):
        return "CData '%s'" % (self.action_point_name)


    @staticmethod
    def getActionPointByID(ap_id):
        return ActionPointDao.query.get(ap_id)

    @staticmethod
    def getAllActionPoints():
        return ActionPointDao.query.order_by(ActionPointToRoleDao.action_point_id)

    @staticmethod
    def createNewActionPoint(name):
        ap = ActionPointDao(name)
        db_session.add(ap)
        db_session.commit()

    @staticmethod
    def updateActionPoint(id, new_name):
        entry = ActionPointDao.get(id)
        entry.name = new_name
        db_session.commit()

    @staticmethod
    def deleteActionPoint(apId):
        remove_role = db_session.query(ActionPointToRoleDao).get(apId)
        db_session.delete(remove_role)
        db_session.commit()
