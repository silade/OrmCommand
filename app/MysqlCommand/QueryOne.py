#!/usr/bin/env python
# encoding: utf-8
"""
@author: leason
@time: 2017/9/29 16:11
"""
from app.untils import operate_commit


class QueryOne:

    request = {}

    def __init__(self, primary_key, response=None):

        self.request['primary_key'] = primary_key
        self.request['response'] = response

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
        else:
            result = 'record is not exited'
        return operate_commit(session), result
