#!/usr/bin/env python
__author__ = 'andrey'

from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, String
from action_point_to_role_dao import Action_point_to_role
from flask import session
from sqlalchemy.orm import relationship, backref
from models import Base


class Action_point(Base):
    __tablename__ = "action_point"

    #action_point_id = Column(Integer, primary_key=True, foreign_key=ForeignKey(Action_point_to_role.action_point_id))
    action_point_id = Column(Integer, primary_key=True)
    action_point_name = Column(String)

    #action_point = relationship(Action_point_to_role, backref=backref('Action_point', lazy='dynamic'))

    def __init__(self, action_point_id, action_point_name):
        self.action_point_id = action_point_id
        self.action_point_name = action_point_name


    def __str__(self):
        return "CData '%s, %s'" % (self.action_point_id, self.action_point_name)


class ActionPointDao(object):

    def __init__(self, action_point_id, action_point_name):
        self.action_point_id = action_point_id
        self.action_point_name = action_point_name

    @staticmethod
    def getActionPointByID(ap_id):
        return session.query(Action_point).get(ap_id)

    @staticmethod
    def getAllActionPoints():
        return session.query(Action_point).order_by(Action_point.action_point_id)

    def createNewActionPoint(self):
        session.add(self)

    def updateActionPoint(self):
        session.commit()

    @staticmethod
    def deleteActionPoint(apId):
        remove_role = session.query(Action_point).get(apId)
        session.delete(remove_role)
        session.commit()
