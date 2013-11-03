#!/usr/bin/env python
__author__ = 'andrey'

from sqlalchemy import Column, Integer, String
from models import Base, session


class RegionDao(Base):
    __tablename__ = "region"

    region_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))

    def __init__(self, region_id, name):
        self.region_id = region_id
        self.name = name

    def __str__(self):
        return "CData '%s, %s'" % (self.region_id, self.name)


    @staticmethod
    def getRegionByID(region_id):
        return session.query(RegionDao).get(region_id)

    @staticmethod
    def getAllRegions():
        return session.query(RegionDao).order_by(RegionDao.region_id)

    @staticmethod
    def createNewRegion(id, name):
        region = RegionDao(id, name)
        session.add(region)
        session.commit()

    @staticmethod
    def updateRegion(id, new_name):
        entry = RegionDao.get(id)
        entry.name = new_name
        session.commit()

    @staticmethod
    def deleteRecord(regionId):
        remove_region = session.query(RegionDao).get(regionId)
        session.delete(remove_region)
        session.commit()
