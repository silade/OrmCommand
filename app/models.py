#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author: leason
@time: 2017/9/8 14:09
"""
from untils import date_time
from sqlalchemy import Column, Integer, String, DateTime
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
    create_time = Column(DateTime,  default=date_time())

    def __init__(self, name=0, des=0):
        self.name = name
        self.des = des

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'create_time': self.create_time,
            'des': self.des
        }

    def __repr__(self):
        return "<id={},name={}>".format(self.id, self.name)




