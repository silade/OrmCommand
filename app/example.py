#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author: leason
@time: 2017/9/8 14:09
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import QueuePool
from MysqlCommand import SingleQuery, MultiQuery, SingleInsert,SingleModify, DeleteOne, DeleteSome, QueryOne

from models import ModelBase
from models import News, Type, Tag

mysql_pool_configs = {
    "url": "mysql+pymysql://root:@127.0.0.1:3306/test?charset=utf8",
    "pool_timeout": 5
}

db_pool = create_engine(mysql_pool_configs['url'], poolclass=QueuePool, echo=True)

session = Session(db_pool)

ModelBase.metadata.create_all(bind=db_pool)


# 添加
def add():
    data = {
        "name": "leason1",
        "des": 123,
    }
    type_add = {
        "type_name": "15161"
    }
    # result = SingleInsert(data).add_method(session, News)
    result = SingleInsert(type_add).add_method(session, Type)
    print result
    return result


# 编辑
def modify():
    data = {
        "primary_key": {
            "id": 10002,
            "name": 10002
        },
        "items": {
            "name": "llx",
            "des": 845
        }
    }
    result = SingleModify(data['primary_key'], data['items']).modify_method(session, News)
    print result
    return result


# 查询详情
def get_one():
    data = {
        "id": 10005
    }

    response = ["name", "des"]

    result, info = QueryOne(data, response).query_method(session, News)
    print info
    return result, info


# 删除
def delete_one():
    data = {
        "id": 10001
    }
    result = DeleteOne(data).delete_method(session, News)
    print result
    return result


# 获取
def get_all():

    request = {
        "cond": {
            "name": "",
            "des": "",
            "create_time": {
                "start_time": "2017-09-19 11:01:21",
                "end_time": "2017-09-26 11:01:22"
            }
        },
        "sort": {
            "name": True
        },
        "limit": 2,
        "page": 1
    }

    response = ["name"]
    request['response'] = ['name', 'des']
    state, sql_total, result = SingleQuery(cond=request['cond'], sort=request['sort'], response=request['response'], limit=10, page=1).query_method(session, News)
    print state
    print sql_total
    print result


# 获取
def get_some_table_all():
    request = {
        "cond": {
            "name": "leas",
            "des": "",
            "create_time": {
                "start_time": "2017-09-19 11:01:21",
                "end_time": "2017-09-26 11:01:22"
            }
        },
        "sort": {
            "name": True
        },
        "response": {
            "news": ["name", "des"],
            "tag": ["tag_name"],
            "type": ["type_name"]
        },
        "limit": 2,
        "page": 1
    }

    state, sql_total, result = MultiQuery(cond=request['cond'], sort=request['sort'], response=request['response'], limit=10, page=1).query_method(session, News, Type, Tag)
    print state
    print sql_total
    print result

if __name__ =='__main__':
    # data = {
    #     "id": 10005
    # }
    add()
    # get_all()
    # get_some_table_all()
    # modify()
    # get_one()
    # delete_one()