#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author: leason
@time: 2017/9/8 14:09
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import QueuePool
from models import News
from models import ModelBase
from sql_opr import add_one, get_detail, del_one, get, modify_one

mysql_pool_configs = {
    "url": "mysql+pymysql://root:@127.0.0.1:3306/test?charset=utf8",
    "pool_timeout": 5
}

db_pool = create_engine(mysql_pool_configs['url'], poolclass=QueuePool, echo=True)

session = Session(db_pool)

ModelBase.metadata.create_all(bind=db_pool)

# 添加
def add(data):
    # data = {
    #     "name": "leason",
    #     "des": "des",
    # }
    result = add_one(session, News, data)
    return result


# 编辑
def modify():
    data = {
        "primary_key": {
            "id": 10002
        },
        "items": {
            "name": "llx",
            "des": 845
        }
    }
    result = modify_one(session, News, data)
    print result
    return result


# 查询
def get_one(data):
    # data = {
    #     "id": 10005
    # }
    result, info = get_detail(session, News, data)
    return result, info

# 删除
def delete_one(data):
    # data = {
    #     "id": 10005
    # }
    result = del_one(session, News, data)
    print result
    return result

# 获取
def get_all():
    data = {
        "cond": {
            "name": "leas",
            "des": ""
        },
        "sort": {
            "name": True
        },
        "limit": 2,
        "page": 1
    }
    result = get(session, News, data)

if __name__ =='__main__':
    data = {
        "id": 10005
    }
    modify()