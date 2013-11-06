#!/usr/bin/env python


# ---Fill test data for user and related entities----
from models.region_dao import RegionDao
from models.role_dao import RoleDao
from models.user_dao import UserDao

RoleDao.createNewRole("Admin")
RegionDao.createNewRegion("Crimea")


UserDao.createNewUser('Login', 'Password','FirstName','LastName', 'Email', 1,1)


for instance in UserDao.getAllUsers():
    print(instance.id,instance.login,instance.password,instance.first_name, instance.last_name, instance.email,
          RoleDao.getRoleByID(instance.role_id).name, RegionDao.getRegionByID(instance.region_id).name)
