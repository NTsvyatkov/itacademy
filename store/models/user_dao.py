#!/usr/bin/env python

from sqlalchemy import ForeignKey, and_
from sqlalchemy import Column, Integer, String
from role_dao import RoleDao
from region_dao import RegionDao
from store.models import Base, db_session
from sqlalchemy.orm import relationship, backref


class UserDao(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True,autoincrement=True)
    login = Column(String(50))
    password = Column(String(50))
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(100))
    role_id = Column(Integer, ForeignKey(RoleDao.role_id))
    region_id = Column(Integer, ForeignKey(RegionDao.region_id))

    role = relationship(RoleDao, backref=backref('user', lazy='dynamic'))
    region = relationship(RegionDao, backref=backref('user', lazy='dynamic'))

    def __init__(self,login, password, first_name, last_name, email, role_id, region_id):
        super(UserDao, self).__init__()
        self.password = password
        self.login = login
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.role_id = role_id
        self.region_id = region_id

    def __str__(self):
        return "CData  '%s, %s, %s, %s, %s, %s, %s, '" % (self.login,
        self.first_name, self.last_name, self.password, self.email, self.region_id, self.role_id)


    @staticmethod
    def  getUserByID(user_id):
        return UserDao.query.get(user_id)

    @staticmethod
    def getAllUsers():
        return UserDao.query.order_by(UserDao.id).all()

    @staticmethod
    def filterUsersByFirstName():
        return UserDao.query.order_by(UserDao.first_name)

    @staticmethod
    def filterUsersByLastName():
        return UserDao.query.order_by(UserDao.last_name)

    @staticmethod
    def filterUsersByEmail():
        return UserDao.query.order_by(UserDao.email)

    @staticmethod
    def filterUsersByRole():
        return UserDao.query.order_by(UserDao.role_id)

    @staticmethod
    def filterUsersByRegion():
        return UserDao.query.order_by(UserDao.region_id)

    @staticmethod
    def createNewUser(login, password, first_name, last_name, email, role_id, region_id):
        user = UserDao(login, password, first_name,last_name,email,role_id,region_id)
        db_session.add(user)
        db_session.commit()

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
        db_session.commit()

    @staticmethod
    def updatePassword(userId, password):
        pst = UserDao.getUserByID(userId)
        pst.password = password
        db_session.commit()

    @staticmethod
    def deleteRecord(userId):
        remove_user = UserDao.getUserByID(userId)
        db_session.delete(remove_user)
        db_session.commit()

    @staticmethod
    def getUserByLogin(userLogin, userPassword):
        posts = UserDao.getAllUsers()
        for instance in posts:
            if instance.login == userLogin and instance.password == userPassword:
            #if  UserDao.query.filter(and_(instance.login == userLogin, instance.password == userPassword)) is not None:
                return UserDao.getUserByID(instance.id)

    @staticmethod
    def isUserExists(userLogin, userPassword):
        user = UserDao.getUserByLogin(userLogin, userPassword)
        result = False
        if user is not None:
            result = True
        return result