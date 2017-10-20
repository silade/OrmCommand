#!/usr/bin/env python
# encoding: utf-8
"""
@author: leason
@time: 2017/10/19 17:11
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import QueuePool
from ..MysqlCommand import SingleQuery, MultiQuery, SingleInsert,SingleModify, DeleteOne, DeleteSome, QueryOne

from ..models import ModelBase
from ..models import News, Type, Tag

# mysql_pool_configs = {
#     "url": "sqlite://"
# }

db = create_engine("sqlite:///:memory:", echo=True)

session = Session(db)

