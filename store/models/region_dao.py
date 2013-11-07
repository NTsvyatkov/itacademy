#!/usr/bin/env python

from sqlalchemy import Column, Integer, String
from store.models import Base, db_session


class RegionDao(Base):
    __tablename__ = "region"

    region_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))

    def __init__(self, name):
        super(RegionDao, self).__init__()
        self.name = name

    def __str__(self):
        return "CData '%s'" % (self.name)


    @staticmethod
    def getRegionByID(region_id):
        return RegionDao.query.get(region_id)

    @staticmethod
    def getAllRegions():
        return RegionDao.query.order_by(RegionDao.region_id)

    @staticmethod
    def createNewRegion(name):
        region = RegionDao(name)
        db_session.add(region)
        db_session.commit()

    @staticmethod
    def updateRegion(id, new_name):
        entry = RegionDao.get(id)
        entry.name = new_name
        db_session.commit()

    @staticmethod
    def deleteRecord(regionId):
        remove_region = db_session.query(RegionDao).get(regionId)
        db_session.delete(remove_region)
        db_session.commit()
