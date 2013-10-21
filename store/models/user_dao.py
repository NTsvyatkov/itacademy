#!/usr/bin/env python
__author__ = 'andrey'

from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, String
from role_dao import Role
from region_dao import Region
from flask import session
from models import Base, db_engine
from sqlalchemy.orm import relationship, backref, sessionmaker

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    login = Column(String(50))
    password = Column(String)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(100))
    role_id = Column(Integer, ForeignKey(Role.role_id))
    region_id = Column(Integer, ForeignKey(Region.region_id))

    #role = relationship(Role, backref=backref(Role, lazy='dynamic'))
    #region = relationship(Region, backref=backref(Region, lazy='dynamic'))

    def __init__(self, id, login, password, first_name, last_name, email, role_id, region_id):
        self.id = id
        self.password = password
        self.login = login
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.role_id = role_id
        self.region_id = region_id

    def __str__(self):
        return "CData '%s, %s, %s, %s, %s, %s, %s, %s, '" % (self.id,
        self.login, self.first_name, self.last_name, self.password, self.email, self.region_id, self.role_id)

Base.metadata.create_all(db_engine)


class UserDao(object):

    def __init__(self, id, login, password, first_name, last_name, email, role_id, region_id):
        self.id = id
        self.login = login
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.role_id = role_id
        self.region_id = region_id

    @staticmethod
    def  getUserByID(user_id):
        return session.query(User).get(user_id)

    @staticmethod
    def getAllUsers():
        return session.query(User).order_by(User.id)

    @staticmethod
    def getUsersByFirstName(first_name):
        return session.query(User).get(first_name)

    @staticmethod
    def getUsersByLastName(last_name):
        return session.query(User).get(last_name)

    @staticmethod
    def getUsersByEmail(email):
        return session.query(User).get(email)

    @staticmethod
    def getUsersByRole(role_id):
        return session.query(User).get(role_id)

    @staticmethod
    def getUsersByRegion(region_id):
        return session.query(User).get(region_id)

    def createNewUser(self):
        session.add(self)
        session.commit()

    def updateUser(self):
        session.commit()

    @staticmethod
    def updatePassword(userId, password):
        pst = session.query(User).filter(User.id == userId).first()
        pst.password = password
        session.commit()

    @staticmethod
    def deleteRecord(userId):
        remove_user = session.query(User).get(userId)
        session.delete(remove_user)
        session.commit()

    @staticmethod
    def getUserByLogin(userLogin):
        posts = session.query(User).all
        for instance in posts:
            if instance.login == userLogin:   #and instance.password == userPassword
                return instance              # instance.password   instance.getLogin / getPassword

    @staticmethod
    def isUserExists(userLogin):
        user = User.getUserByLogin(userLogin)
        result = False
        if user!= None:
            result = True
        return result
