#!/usr/bin/env python

from sqlalchemy import ForeignKey, and_, asc
from sqlalchemy import Column, Integer, String, DECIMAL
from role_dao import RoleDao
from region_dao import RegionDao
from models import Base, db_session
from sqlalchemy.orm import relationship, backref
import hashlib



class Security(Base):
    __tablename__ = "security"
    id = Column(Integer, primary_key=True,autoincrement=True)
    failed_attempts = Column(Integer(20))
    max_attempts = Column(Integer(20))

    def __init__(self,failed_attempts,max_attempts):
        super(Security, self).__init__()
        self.failed_attempts = failed_attempts
        self.max_attempts = max_attempts

    @staticmethod
    def add_security(failed_attempts, max_attempts):
        security = Security(failed_attempts, max_attempts)
        db_session.add(security)
        db_session.commit()

    @staticmethod
    def getSecuritybyId(id):
        return Security.query.get(id)

    @staticmethod
    def getSecyrity():
        return Security.query.all()

    @staticmethod
    def updateSecurity(id,failed_attempts, max_attempts):
        entry = Security.getSecuritybyId(id)
        entry.failed_attempts = failed_attempts
        entry.max_attempts = max_attempts
        db_session.commit()


class UserLevel(Base):
    __tablename__ = "user_level"
    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(50))
    balance = Column(DECIMAL(7,2))
    discount = Column(Integer)

    def __init__(self,name,balance, discount):
        super(UserLevel, self).__init__()
        self.name = name
        self.balance = balance
        self.discount = discount

    @staticmethod
    def add_user_level(name, balance, discount):
        user_level = UserLevel(name, balance, discount)
        db_session.add(user_level)
        db_session.commit()

    # Get level by level name
    @staticmethod
    def get_level_by_name(name):
        return UserLevel.query.filter(UserLevel.name == name).first()

    # Get level id by level name
    @staticmethod
    def get_level_id_by_name(name):
        entry = UserLevel.query.filter(UserLevel.name == name).first()
        return entry.id


class UserDao(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True,autoincrement=True)
    login = Column(String(50), unique=True)
    password = Column(String(50))
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(100), unique=True)
    role_id = Column(Integer, ForeignKey(RoleDao.role_id))
    region_id = Column(Integer, ForeignKey(RegionDao.region_id))
    role = relationship(RoleDao, backref=backref('user', lazy='dynamic'))
    region = relationship(RegionDao, backref=backref('user', lazy='dynamic'))
    level_id = Column(Integer, ForeignKey(UserLevel.id))
    level = relationship(UserLevel, backref=backref('user', lazy='dynamic'))
    balance = Column(DECIMAL(7, 2))

    def __init__(self, login, password, first_name, last_name, email, role_id, region_id, level_id=None, balance=None):
        super(UserDao, self).__init__()
        self.password = password
        self.login = login
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.role_id = role_id
        self.region_id = region_id
        self.level_id = level_id
        self.balance = balance

    def __str__(self):
        return "CData  '%s, %s, %s, %s, %s, %s, %s, '" % (self.login, self.password,
        self.first_name, self.last_name, self.email, self.region_id, self.role_id)

    @staticmethod
    def getUserByID(user_id):
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
        user = UserDao(login, hashlib.md5(password).hexdigest(), first_name, last_name, email, role_id, region_id)
        if role_id == RoleDao.get_role_id_by_name("Customer"):
            user.level_id = UserLevel.get_level_id_by_name("Standard")
            user.balance = 0
        db_session.add(user)
        db_session.commit()

    @staticmethod
    def updateUser(id, login, password, first_name, last_name, email, role_id, region_id):
        entry = UserDao.getUserByID(id)
        entry.login = login
        entry.password = hashlib.md5(password).hexdigest()
        entry.first_name = first_name
        entry.last_name = last_name
        entry.email = email
        entry.role_id = role_id
        entry.region_id = region_id
        db_session.commit()

    @staticmethod
    def updatePassword(userId, password):
        pst = UserDao.getUserByID(userId)
        pst.password = hashlib.md5(password).hexdigest()
        db_session.commit()

    @staticmethod
    def deleteRecord(userId):
        remove_user = UserDao.getUserByID(userId)
        db_session.delete(remove_user)
        db_session.commit()

    @staticmethod
    def getUserByLogin(userLogin, userPassword):
        return UserDao.query.filter(and_(UserDao.login == userLogin,
                                         UserDao.password == hashlib.md5(userPassword).hexdigest())).first()
    @staticmethod
    def getUserByRole(role):
        return UserDao.query.filter(UserDao.role_id == role).all()

    @staticmethod
    def getUserByRoleName(role_name):
        return UserDao.query.join(UserDao.role).filter(RoleDao.name == role_name).all()

    @staticmethod
    def isUserExists(userLogin, userPassword):
        user = UserDao.getUserByLogin(userLogin, userPassword)
        result = False
        if user is not None:
            result = True
        return result

    @staticmethod
    def pagerByFilterUsers(page=None, records_per_page=None, search_field=None, search_criteria=None, search_value = None):
        query = UserDao.query


        if search_value:
            if search_field =='login':
                f = UserDao.login
            elif search_field == 'first_name':
                f = UserDao.first_name
            elif search_field == 'last_name':
                f = UserDao.last_name
            elif search_field =='email':
                f = UserDao.email


            if search_criteria == 'start_with':
                query = query.filter(f.like(search_value + '%'))
            elif search_criteria =='equals':
                query = query.filter(f == search_value)
            elif search_criteria =='contains':
                query = query.filter(f.contains(search_value))

        stop = page * records_per_page
        start = stop - records_per_page
        return query.order_by(UserDao.id).slice(start, stop), \
            query.count()
        

    @staticmethod
    def get_user_info_by_id(user_id):
        entry = {}
        query = UserDao.query.get(user_id)
        entry["user_login"] = query.login
        entry["user_first_name"] = query.first_name
        entry["user_last_name"] = query.last_name
        entry["user_role"] = query.role.name
        if entry["user_role"] == "Customer":
            entry["user_level"] = query.level.name
            entry["user_balance"] = str(query.balance)
            next_level = UserLevel.query.filter(UserLevel.balance > entry["user_balance"]).\
                order_by(asc(UserLevel.balance)).first()
            if next_level:
                entry["user_next_level"] = next_level.name
                user_next_balance = str(next_level.balance)
                entry["user_must_spend"] = float(user_next_balance) - float(entry["user_balance"])
        return entry
