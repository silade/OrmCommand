#!/usr/bin/env python
# encoding: utf-8
"""
@author: leason
@time: 2017/9/28 17:42
"""
from app.untils import operate_commit


def single_insert_validate(func):
    def inner(request, session, orm):
        data = request.request
        # 校验Orm 需要有构造方法和to_json方法
        if 'to_json' not in orm.__dict__.keys() or '__init__' not in orm.__dict__.keys():
            raise Exception(orm.__name__ + ' must have methods __init__ and to_json')

        # 校验data字段类型为dict并且orm有字段内属性
        if not isinstance(data, dict):
            raise TypeError('data must be dict')
        else:
            for key in data:
                if not hasattr(orm, key):
                    raise AttributeError(orm.__name__ + ' has no attribute "' + key + '"')

        return func(request, session, orm)
    return inner


class SingleInsert:
    request = {

    }

    def __init__(self, data):
        self.request = data

    @single_insert_validate
    def add_method(self, session, orm):
        """
        通用插入数据方法
        :type session:
        :param session: 数据库连接

        :type orm: class
        :param orm: model类 --该类需要有构造方法

        :type datas: dict
        :param datas:{
            "a":"b",
            "c":1
        }

        :rtype: Boolean
        :return:True or False
        """
        data = self.request
        # 兼容Orm有初始化参数和无初始化参数
        try:
            model = orm(**data)
        except:
            model = orm()
            for key, value in data.items():
                setattr(model, key, value)

        session.add(model)
        return operate_commit(session)
