#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author: leason
@time: 2017/9/8 14:09
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
ModelBase = declarative_base()


class News(ModelBase):
    __tablename__ = "news"
    __table_args__ = {
        'mysql_auto_increment': '10001'
    }

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=50))
    des = Column(Integer)

    def __init__(self, name=0, des=0):
        self.name = name
        self.des = des

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'des': self.des
        }

    def __repr__(self):
        return "<id={},name={}>".format(self.id, self.name)