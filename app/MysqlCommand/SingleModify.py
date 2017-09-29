#!/usr/bin/env python
# encoding: utf-8
"""
@author: leason
@time: 2017/9/29 9:43
"""
from app.untils import operate_commit


def single_modify_validate(func):
    def inner(request, session, orm):
        data = request.request
        # 校验Orm 需要有构造方法和to_json方法
        if 'to_json' not in orm.__dict__.keys() or '__init__' not in orm.__dict__.keys():
            raise Exception(orm.__name__ + ' must have methods __init__ and to_json')

        # 校验data字段类型为dict并且orm有字段内属性
        if not isinstance(data, dict):
            raise TypeError('data must be dict')
        else:
            pass

        return func(request, session, orm)
    return inner


class SingleModify:
    request = {

    }

    def __init__(self, data):
        self.request = data

    @single_modify_validate
    def modify_method(self, session, orm):
        """
        通用编辑方法
        :type session:
        :param session: 数据库连接

        :type orm: class
        :param orm: model类 --该类需要有构造方法

        :type data: dict
        :param data:{
            "primary_key":{
                "id":10006
            },
            "items":{
                "name":"llx"
            }
        }

        :rtype: Boolean, str or dict
        :return:True or False, str or dict
        """
        data = self.request
        primary_key = data['primary_key']
        items = data['items']
        # 获取查询key
        primary_key_key, key_value = primary_key.items()[0]

        ret_key = getattr(orm, primary_key_key)

        sql_result = session.query(orm).filter(ret_key == key_value).one_or_none()
        if sql_result:
            for item_key, item_value in items.items():
                setattr(sql_result, item_key, item_value)
            return operate_commit(session)
        else:
            return 'record is not exited'
