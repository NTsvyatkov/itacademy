#!/usr/bin/env python
__author__ = 'andrey'

from sqlalchemy import Column, Integer, String
from flask import session
from models import Base


class Region(Base):
    __tablename__ = "region"

    region_id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(50))

    def __init__(self, region_id, name):
        self.region_id = region_id
        self.name = name

    def __str__(self):
        return "CData '%s, %s'" % (self.region_id, self.name)


class RegionDao(object):

    def __init__(self, region_id, name):
        self.region_id = region_id
        self.name = name

    @staticmethod
    def getRegionByID(region_id):
        return session.query(Region).get(region_id)

    @staticmethod
    def getAllRegions():
        return session.query(Region).order_by(Region.region_id)

    def createNewRegion(self):
        session.add(self)

    def updateRegion(self):
        session.commit()

    @staticmethod
    def deleteRecord(regionId):
        remove_region = session.query(Region).get(regionId)
        session.delete(remove_region)
        session.commit()
