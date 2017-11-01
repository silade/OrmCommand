#!/usr/bin/env python
# encoding: utf-8
"""
@author: leason
@time: 2017/10/13 15:56
"""
from Utils.utils import operate_commit


def delete_some_validate(func):
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

            # 校验所有的id值是list
            if not isinstance(value, list):
                raise TypeError('primary_key\'s value must be list')

        return func(request, session, orm)
    return inner


class DeleteSome:
    request = {

    }

    def __init__(self, primary_key):
        self.request = primary_key

    @delete_some_validate
    def delete_method(self, session, orm):
        """
        通用删除多条数据方法
        :type session:
        :param session: 数据库连接

        :type orm: class
        :param orm: model类 --该类需要有构造方法

        :type datas: dict
        :param datas:{
            "user_id":['123','321']
        }

        :rtype: Boolean, str or dict
        :return:True or False, str or dict
        """
        data = self.request
        key, value = data.items()[0]

        ret = getattr(orm, key)

        for i in value:
            sql_result = session.query(orm).filter(ret == i)
            if sql_result.count() is 1:
                session.delete(sql_result.one())
            else:
                session.close()
                return 'record is not exited'
        result = operate_commit(session)
        return result
