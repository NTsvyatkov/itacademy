#!/usr/bin/env python


from business_logic.user_manager import validationRegionID
from models.region_dao import RegionDao
from validation import ValidationException


def validationRegionName(region_name):
    if region_name is None:
        raise ValidationException("The region name is required field")
    elif len(region_name) > 50:
        raise ValidationException("Name length should be no more than 50 characters")


def getlistRegion():
    return RegionDao.getAllRegions()


def createRegion(region_id, name):
    validationRegionName(name)
    RegionDao.createNewRegion(region_id, name)


def updateRegion(region_id, name):
    validationRegionID(region_id)
    validationRegionName(name)
    RegionDao.updateRegion(region_id, name)


def deleteRegion(region_id):
    validationRegionID(region_id)
    RegionDao.deleteRecord(region_id)


def getRegionByID(region_id):
    validationRegionID(region_id)
    return RegionDao.getRegionByID(region_id)




