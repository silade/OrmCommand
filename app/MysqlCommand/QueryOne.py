#!/usr/bin/env python
# encoding: utf-8
"""
@author: leason
@time: 2017/9/29 16:11
"""
from Untils.untils import operate_commit


def query_one_validate(func):
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
            all_key = [primary_key for primary_key, _ in data['primary_key'].items()] + [key_res for key_res in
                                                                                         data['response']]
            for key in all_key:
                if not hasattr(orm, key):
                    raise AttributeError(orm.__name__ + ' has no attribute "' + key + '"')

        return func(request, session, orm)
    return inner


class QueryOne:

    request = {}

    def __init__(self, primary_key, response=None):

        self.request['primary_key'] = primary_key
        self.request['response'] = response

    @query_one_validate
    def query_method(self, session, orm):
        """
        通用查询数据详情方法
        :type session:
        :param session: 数据库连接

        :type orm: class
        :param orm: model类 --该类需要有构造方法

        :type data: dict
        :param data:{
            "primary_key":{
                "id":10006
            },
            "response":[
                "name",
                "des"
            ]
        }

        :rtype: Boolean, str or dict
        :return:True or False, str or dict
        """
        data = self.request
        key, value = data['primary_key'].items()[0]

        ret = getattr(orm, key)

        sql_result = session.query(orm).filter(ret == value)
        if sql_result.count() is 1:
            result_content = sql_result.one()
            # 判断是否自定义response
            if data['response']:
                result = {res_key: getattr(result_content, res_key) for res_key in data['response']}
            else:
                # 返回所有
                result = result_content.to_json()
            state = operate_commit(session)
        else:
            operate_commit(session)
            result = 'record is not exited'
            state = False
        return state, result
