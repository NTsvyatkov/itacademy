#!/usr/bin/env python

from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, String
from role_dao import RoleDao
from region_dao import RegionDao
from flask import session
from models import Base
from sqlalchemy.orm import relationship, backref

class UserDao(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    login = Column(String(50))
    password = Column(String(50))  # fix maxleng
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(100))
    role_id = Column(Integer, ForeignKey(RoleDao.role_id))
    region_id = Column(Integer, ForeignKey(RegionDao.region_id))

    role = relationship(RoleDao, backref=backref('user', lazy='dynamic'))
    region = relationship(RegionDao, backref=backref('user', lazy='dynamic'))

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

    #Base.metadata.create_all(db_engine)

    @staticmethod
    def  getUserByID(user_id):
        return session.query(UserDao).get(user_id)

    @staticmethod
    def getAllUsers():
        return session.query(UserDao).order_by(UserDao.id)

    @staticmethod
    def getUsersByFirstName(first_name):
        return session.query(UserDao).get(first_name)

    @staticmethod
    def getUsersByLastName(last_name):
        return session.query(UserDao).get(last_name)

    @staticmethod
    def getUsersByEmail(email):
        return session.query(UserDao).get(email)

    @staticmethod
    def getUsersByRole(role_id):
        return session.query(UserDao).get(role_id)

    @staticmethod
    def getUsersByRegion(region_id):
        return session.query(UserDao).get(region_id)

    @staticmethod
    def createNewUser(id, login, password, first_name, last_name, email, role_id, region_id):
        user = UserDao(id,login,password,first_name,last_name,email,role_id,region_id)
        session.add(user)
        session.commit()

    @staticmethod
    def updateUser(id, login, password, first_name, last_name, email, role_id, region_id):
        entry = UserDao.getUserByID(id)
        entry.login = login
        entry.password = password
        entry.first_name = first_name
        entry.last_name = last_name
        entry.email = email
        entry.role_id = role_id
        entry.region_id = region_id
        session.commit()

    @staticmethod
    def updatePassword(userId, password):
        pst = session.query(UserDao).filter(UserDao.id == userId).first()
        pst.password = password
        session.commit()

    @staticmethod
    def deleteRecord(userId):
        remove_user = session.query(UserDao).get(userId)
        session.delete(remove_user)
        session.commit()

    @staticmethod
    def getUserByLogin(userLogin):
        posts = session.query(UserDao).all
        for instance in posts:
            if instance.login == userLogin:   #and instance.password == userPassword
                return instance              # instance.password   instance.getLogin / getPassword

    @staticmethod
    def isUserExists(userLogin):
        user = UserDao.getUserByLogin(userLogin)
        result = False
        if user!= None:
            result = True
        return result
