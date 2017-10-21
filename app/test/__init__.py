#!/usr/bin/env python
# encoding: utf-8
"""
@author: leason
@time: 2017/10/19 17:11
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from ..MysqlCommand import SingleQuery, MultiQuery, SingleInsert, SingleModify, DeleteOne, DeleteSome, QueryOne

from ..models import ModelBase
from ..models import News, Type, Tag

db = create_engine("sqlite:///:memory:", echo=True)

session = Session(db)

ModelBase = ModelBase

News, Type, Tag = News, Type, Tag

SingleQuery, MultiQuery, SingleInsert, SingleModify, DeleteOne, DeleteSome, QueryOne = SingleQuery, MultiQuery, SingleInsert,SingleModify, DeleteOne, DeleteSome, QueryOne

