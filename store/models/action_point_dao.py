#!/usr/bin/env python
__author__ = 'andrey'
from sqlalchemy import ForeignKey
from action_point_to_role_dao import ActionPointToRoleDao
from models import Base, session, engine
from sqlalchemy import Column, Date, Integer, String, DATE, ForeignKey, Text, Float
from sqlalchemy.orm import relationship, backref



class ActionPointDao(Base):
    __tablename__ = "action_point"

    action_point_id = Column(Integer, ForeignKey('action_point_to_role.ap_to_role_id'), primary_key=True ,
                             autoincrement=True)
    action_point_name = Column(String)

    action_point = relationship(ActionPointToRoleDao, backref=backref('action_point', lazy='dynamic'))


    def __init__(self, action_point_id, action_point_name):
        self.action_point_id = action_point_id
        self.action_point_name = action_point_name


    def __str__(self):
        return "CData '%s, %s'" % (self.action_point_id, self.action_point_name)


    @staticmethod
    def getActionPointByID(ap_id):
        return session.query(ActionPointToRoleDao).get(ap_id)

    @staticmethod
    def getAllActionPoints():
        return session.query(ActionPointToRoleDao).order_by(ActionPointToRoleDao.action_point_id)

    @staticmethod
    def createNewActionPoint(id, name):
        ap = ActionPointDao(id, name)
        session.add(ap)
        session.commit()

    @staticmethod
    def updateActionPoint(id, new_name):
        entry = ActionPointDao.get(id)
        entry.name = new_name
        session.commit()

    @staticmethod
    def deleteActionPoint(apId):
        remove_role = session.query(ActionPointToRoleDao).get(apId)
        session.delete(remove_role)
        session.commit()
