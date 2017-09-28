#!/usr/bin/env python
# encoding: utf-8
"""
@author: leason
@time: 2017/9/27 14:13
"""
from app.untils import operate_commit
from sqlalchemy import and_


def single_query_validate(func):
    def inner(request, session, orm):
        data = request.request
        # 校验Orm 需要有构造方法和to_json方法
        if 'to_json' not in orm.__dict__.keys() or '__init__' not in orm.__dict__.keys():
            raise Exception('Orm must have methods __init__ and to_json')

        # 校验limit和page字段类型为int
        if not isinstance(data['limit'], int) or not isinstance(data['page'], int):
            raise TypeError('limit and page must be int')

        # 校验cond和sort字段类型为dict 、校验cond和sort里的属性是否存在orm类里
        if not isinstance(data['cond'], dict) or not isinstance(data['sort'], dict):
            raise TypeError('cond and sort must be dict')

        # 校验response字段类型为list和校验response里的属性是否存在orm类里
        if not isinstance(data['response'], list):
            raise TypeError('response must be list')

        # 校验所有的key是不是都是orm的属性
        all_key = [key_sort for key_sort, _ in data['sort'].items()] + [key_cond for key_cond, _ in data['cond'].items()] + [key_response for key_response in data['response']]
        for key in all_key:
            if not hasattr(orm, key):
                raise AttributeError(orm.__name__ + ' has no attribute "' + key + '"')

        return func(request, session, orm)
    return inner


class SingleQuery:

    request = {

    }

    def __init__(self, cond, sort, response, limit=10, page=1):
        self.request['cond'] = cond
        self.request['sort'] = sort
        self.request['response'] = response
        self.request['limit'] = limit
        self.request['page'] = page

    @single_query_validate
    def query_method(self, session, orm):
        """
        通用查询数据详情方法
        :type session:
        :param session: 数据库连接

        :type orm: class
        :param orm: model类 --该类需要有构造方法

        :type reuqest: dict
        :param reuqest:{
            "cond": {
                "name": "leas",
                "des": "",
                "create_time":{
                    "start_time":"2017-09-11 11:56:22",
                    "end_time":"2017-09-11 11:56:22"
                }
            },
            "sort": {
                "name": True
            },
            "response":["name", "des"]  #需要返回的的数据
            "limit": 2,
            "page": 1
        }

        :rtype: Boolean, Int , list[dict]
        :return:True or False, Int, list[dict]
        """
        request = self.request
        # 返回的list
        response = request['response']

        # 分页
        limit = request['limit']
        offset = (request['page'] - 1) * request['limit']

        # &&条件
        cond = request['cond']
        sql_cond = []
        for key, value in cond.items():
            ret = getattr(orm, key)
            # 判断是不是时间段条件
            # 时间段字段key字符串必须包含'time'字符串
            if isinstance(value, dict) and 'time' in key:
                sql_cond.append(ret.between(value.values()[0], value.values()[1]))
            else:
                sql_cond.append(ret.like('%' + str(value) + '%') if value is not None else "")

        condition = and_(
            *sql_cond
        )

        # 排序
        sort = request['sort']  # key 排序字段  True 降序 False 升序
        sort_key, sort_value = sort.items()[0]
        sort_ret = getattr(orm, sort_key)
        if sort_value:
            sort_ret = sort_ret.desc()

        sql_result = session.query(orm).filter(
            condition
        )
        sql_content = sql_result.order_by(sort_ret).limit(limit).offset(offset)
        sql_total = sql_result.count()
        # 如果不添加返回字段，返回所有
        if response:
            result = []
            for i in sql_content:
                c = {}
                for res_key in response:
                    c[res_key] = getattr(i, res_key)
                result.append(c)
        else:
            result = [i.to_json() for i in sql_content]

        return operate_commit(session), sql_total, result
