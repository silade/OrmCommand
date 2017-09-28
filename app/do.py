#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author: leason
@time: 2017/9/8 14:09
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import QueuePool

from app.MysqlCommand.SingleQuery import SingleQuery
from app.MysqlCommand.MultiQuery import MultiQuery
from models import ModelBase
from models import News, Type, Tag
from sql_opr import add_one, get_detail, del_one, modify_one, multi_table_list

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
        "name": "leason",
        "des": 123,
    }
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
    # state, sql_total, result = single_table_list(session, News, request)
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
    orms = [News, Type, Tag]
    state, sql_total, result = MultiQuery(cond=request['cond'], sort=request['sort'], response=request['response'], limit=10, page=1).query_method(session, News, Type, Tag)
    print state
    print sql_total
    print result

if __name__ =='__main__':
    # data = {
    #     "id": 10005
    # }
    # add()
    # get_all()
    get_some_table_all()