#!/usr/bin/env python
# encoding: utf-8
"""
@author: leason
@time: 2017/9/28 9:33
"""
from sqlalchemy import and_

from Untils.untils import operate_commit


def multi_query_validate(func):
    def inner(request, session, *orm):
        data = request.request

        # 校验orm为list 需要有构造方法和to_json方法
        if not isinstance(orm, tuple):
            raise TypeError('orm must be tuple')
        else:
            for orm_one in orm:
                if 'to_json' not in orm_one.__dict__.keys() or '__init__' not in orm_one.__dict__.keys():
                    raise Exception(orm_one.__name__ + ' must have methods __init__ and to_json')
                else:
                    # 校验response字段类型为dict和校验response里的属性是否存在orm类里
                    if not isinstance(data['response'], dict):
                        raise TypeError('response must be list')

                    # 校验orm和response的长度是否相等
                    if len(data['response']) is not len(orm):
                        raise Exception('response and orm must be equal in length')

                    # 校验response字段对应类的属性
                    for key_response in data['response'][orm_one.__tablename__]:
                        if not hasattr(orm_one, key_response):
                            raise AttributeError(orm_one.__name__ + ' has no attribute "' + key_response + '"')

        # 校验limit和page字段类型为int
        if not isinstance(data['limit'], int) or not isinstance(data['page'], int):
            raise TypeError('limit and page must be int')

        # 校验cond和sort字段类型为dict 、校验cond和sort里的属性是否存在orm类里
        if not isinstance(data['cond'], dict) or not isinstance(data['sort'], dict):
            raise TypeError('cond and sort must be dict')

        # 校验所有的key是不是都是orm的属性
        all_key = [key_sort for key_sort, _ in data['sort'].items()] + [key_cond for key_cond, _ in
                                                                        data['cond'].items()]
        for key in all_key:
            if not hasattr(orm[0], key):
                raise AttributeError(orm[0].__name__ + ' has no attribute "' + key + '"')

        return func(request, session, *orm)
    return inner


class MultiQuery:

    request = {

    }

    def __init__(self, cond,  response, sort={}, limit=0, page=1):
        self.request['cond'] = cond
        self.request['sort'] = sort
        self.request['response'] = response
        self.request['limit'] = limit
        self.request['page'] = page

    @multi_query_validate
    def query_method(self, session, *orm):
        """
        通用联表查询数据详情方法
        :type session:
        :param session: 数据库连接

        :type Orm: list[class]
        :param Orm: model类 --list[0]主表

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
            "response":{
                "news":["name", "des"],
                "tag":["tag_name"],
                "type":["type_name"]
            },                               #需要返回的的数据
            "sort": {
                "name": True
            },
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
        main_orm = orm[0]
        for key, value in cond.items():
            ret = getattr(main_orm, key)
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
        if sort:
            sort_key, sort_value = sort.items()[0]
            sort_ret = getattr(main_orm, sort_key)
            if sort_value:
                sort_ret = sort_ret.desc()
        else:
            sort_ret = None
        # 联表
        sql_result = session.query(*orm).join(*orm[1:], isouter=True).filter(
            condition
        )
        # 0为False
        if limit:
            sql_content = sql_result.order_by(sort_ret).limit(limit).offset(offset)
        else:
            sql_content = sql_result.order_by(sort_ret)
        sql_total = sql_result.count()
        result = []
        for i in sql_content:
            try:
                # 多表情况
                c = {}
                for a in i:
                    if a:
                        # 判断是否有返回字段
                        if response[a.__tablename__]:
                            c[a.__tablename__] = {}
                            for res_key in response[a.__tablename__]:
                                c[a.__tablename__][res_key] = getattr(a, res_key)
                        else:
                            # 使用表名作为key
                            c[a.__tablename__] = a.to_json()
                result.append(c)
            except:
                # 单表情况
                if response[i.__tablename__]:
                    c = {}
                    for res_key in response[i.__tablename__]:
                        c[res_key] = getattr(i, res_key)
                    result.append(c)
                else:
                    result.append(i.to_json())
        return operate_commit(session), sql_total, result
