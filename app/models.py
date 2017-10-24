#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author: leason
@time: 2017/9/8 14:09
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from app.MysqlCommand.Untils.untils import date_time

ModelBase = declarative_base()


class News(ModelBase):
    __tablename__ = "news"
    __table_args__ = {
        'mysql_auto_increment': '10001'
    }

    id = Column(Integer, primary_key=True)
    # type_id = Column(Integer)
    # tag_id = Column(Integer)
    type_id = Column(Integer, ForeignKey('type.id', ondelete='CASCADE', onupdate='CASCADE'))
    tag_id = Column(Integer, ForeignKey('tag.id', ondelete='CASCADE', onupdate='CASCADE'))
    name = Column(String(length=50))
    des = Column(Integer)
    create_time = Column(String(length=50),  default=date_time())

    def __init__(self, name, des, type_id=None, tag_id=None):
        self.name = name
        self.type_id = type_id
        self.tag_id = tag_id
        self.des = des
        self.create_time = date_time()

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'type_id': self.type_id,
            'tag_id': self.tag_id,
            'create_time': str(self.create_time),
            'des': self.des
        }

    def __repr__(self):
        return "<id={},name={}>".format(self.id, self.name)


class Type(ModelBase):
    __tablename__ = "type"
    __table_args__ = {
        'mysql_auto_increment': '10001'
    }

    id = Column(Integer, primary_key=True)
    type_name = Column(String(length=50))
    create_time = Column(String(length=50), default=date_time())

    def __init__(self, type_name=0):
        self.type_name = type_name
        self.create_time = date_time()

    def to_json(self):
        return {
            'id': self.id,
            'type_name': self.type_name,
            'create_time': str(self.create_time)
        }

    def __repr__(self):
        return "<id={},type_name={}>".format(self.id, self.type_name)


class Tag(ModelBase):
    __tablename__ = "tag"
    __table_args__ = {
        'mysql_auto_increment': '10001'
    }

    id = Column(Integer, primary_key=True)
    tag_name = Column(String(length=50))
    create_time = Column(String(length=50), default=date_time())

    def __init__(self, tag_name=0):
        self.tag_name = tag_name
        self.create_time = date_time()

    def to_json(self):
        return {
            'id': self.id,
            'tag_name': self.tag_name,
            'create_time': str(self.create_time)
        }

    def __repr__(self):
        return "<id={},tag_name={}>".format(self.id, self.tag_name)