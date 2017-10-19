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

mysql_pool_configs = {
    "url": "mysql+pymysql://root:@127.0.0.1:3306/test?charset=utf8",
    "pool_timeout": 5
}

db_pool = create_engine(mysql_pool_configs['url'], poolclass=QueuePool, echo=True)

session = Session(db_pool)

ModelBase.metadata.create_all(bind=db_pool)