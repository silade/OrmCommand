#!/usr/bin/env python
# encoding: utf-8
"""
@author: leason
@time: 2017/9/29 16:51
"""
from Utils.utils import operate_commit


def delete_one_validate(func):
    def inner(request, session, orm):
        data = request.request
        # 校验Orm 需要有构造方法和to_json方法
        if 'to_json' not in orm.__dict__.keys() or '__init__' not in orm.__dict__.keys():
            raise Exception(orm.__name__ + ' must have methods __init__ and to_json')

        # 校验data字段类型为dict并且orm有字段内属性
        if not isinstance(data, dict):
            raise TypeError('data must be dict')
        else:
            # 校验所有的key是不是都是orm的属性
            key, value = data.items()[0]
            if not hasattr(orm, key):
                raise AttributeError(orm.__name__ + ' has no attribute "' + key + '"')

        return func(request, session, orm)
    return inner


class DeleteOne:
    request = {

    }

    def __init__(self, primary_key):
        self.request = primary_key

    @delete_one_validate
    def delete_method(self, session, orm):
        """
        通用删除数据方法
        :type session:
        :param session: 数据库连接

        :type orm: class
        :param orm: model类 --该类需要有构造方法

        :type datas: dict
        :param datas:{
            "user_id":6156161
        }

        :rtype: Boolean, str or dict
        :return:True or False, str or dict
        """
        data = self.request
        key, value = data.items()[0]

        ret = getattr(orm, key)

        sql_result = session.query(orm).filter(ret == value)
        if sql_result.count() is 1:
            session.delete(sql_result.one())
            result = operate_commit(session)
        else:
            operate_commit(session)
            result = 'record is not exited'
        return result
