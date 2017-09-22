#!/usr/bin/env python
# encoding: utf-8
"""
@author: leason
@time: 2017/9/15 11:12
"""
from sqlalchemy import and_
from validate import validate


# 插入记录
@validate
def add_one(session, Orm, datas):
    """
    通用插入数据方法
    :type session:
    :param session: 数据库连接

    :type Orm: class
    :param Orm: model类 --该类需要有构造方法

    :type datas: dict
    :param datas:{
        "a":"b",
        "c":1
    }

    :rtype: Boolean
    :return:True or False
    """
    # 兼容Orm有初始化参数和无初始化参数
    try:
        model = Orm(**datas)
    except:
        model = Orm()
        for key, value in datas.items():
            setattr(model, key, value)

    session.add(model)
    return __oprate_commit(session)


# 编辑记录
@validate
def modify_one(session, Orm, datas):
    """
    通用编辑方法
    :type session:
    :param session: 数据库连接

    :type Orm: class
    :param Orm: model类 --该类需要有构造方法

    :type datas: dict
    :param datas:{
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
    primary_key = datas['primary_key']
    items = datas['items']
    # 获取查询key
    primary_key_key, key_value = primary_key.items()[0]

    ret_key = getattr(Orm, primary_key_key)

    sql_result = session.query(Orm).filter(ret_key == key_value).one_or_none()
    if sql_result:
        for item_key, item_value in items.items():
            setattr(sql_result, item_key, item_value)
        return __oprate_commit(session)
    else:
        return 'record is not exited'


# 获取记录详情
@validate
def get_detail(session, Orm, datas):
    """
    通用查询数据详情方法
    :type session:
    :param session: 数据库连接

    :type Orm: class
    :param Orm: model类 --该类需要有构造方法

    :type datas: dict
    :param datas:{
        "user_id":6156161
    }

    :rtype: Boolean, str or dict
    :return:True or False, str or dict
    """
    key, value = datas.items()[0]

    ret = getattr(Orm, key)

    sql_result = session.query(Orm).filter(ret == value)
    if sql_result.count() is 1:
        result_content = sql_result.one()
        result = result_content.to_json()
    else:
        result = 'record is not exited'
    return __oprate_commit(session), result


# 删除记录
@validate
def del_one(session, Orm, datas):
    """
    通用查询数据详情方法
    :type session:
    :param session: 数据库连接

    :type Orm: class
    :param Orm: model类 --该类需要有构造方法

    :type datas: dict
    :param datas:{
        "user_id":6156161
    }

    :rtype: Boolean, str or dict
    :return:True or False, str or dict
    """
    key, value = datas.items()[0]

    ret = getattr(Orm, key)

    sql_result = session.query(Orm).filter(ret == value)
    if sql_result.count() is 1:
        session.delete(sql_result.one())
        return __oprate_commit(session)
    else:
        result = 'record is not exited'
        return result


# 单表多条件&&组合查询多条记录
@validate
def get(session, Orm, datas):
    """
    通用查询数据详情方法
    :type session:
    :param session: 数据库连接

    :type Orm: class
    :param Orm: model类 --该类需要有构造方法

    :type datas: dict
    :param datas:{
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
        "limit": 2,
        "page": 1
    }

    :rtype: Boolean, Int , list[dict]
    :return:True or False, Int, list[dict]
    """
    # 分页
    limit = datas['limit']
    offset = (datas['page'] - 1) * datas['limit']

    # &&条件
    cond = datas['cond']
    sql_cond = []
    for key, value in cond.items():
        ret = getattr(Orm, key)
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
    sort = datas['sort']    # key 排序字段  True 降序 False 升序
    sort_key, sort_value = sort.items()[0]
    sort_ret = getattr(Orm, sort_key)
    if sort_value:
        sort_ret = sort_ret.desc()

    sql_result = session.query(Orm).filter(
        condition
    )
    sql_content = sql_result.order_by(sort_ret).limit(limit).offset(offset)
    sql_total = sql_result.count()
    result = [i.to_json() for i in sql_content]
    return __oprate_commit(session), sql_total, result


# 联表&多条件查询
def get_some_table():
    pass


# 数据库session提交回滚操作
def __oprate_commit(fun):
    try:
        fun.commit()
        fun.close()
        return True
    except:
        fun.rollback()
        return False


