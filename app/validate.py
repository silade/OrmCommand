#!/usr/bin/env python
# encoding: utf-8
"""
@author: leason
@time: 2017/9/20 16:06
"""


def validate(func):
    def inner(session, Orm, datas):
        # 校验datas -- dict
        if type(datas) is not dict:
            raise TypeError('datas must be dict')
        # 校验Orm 需要无构造函数或无构造参数
        try:
            Orm()
        except Exception:
            raise Exception('Orm must have no __init__() or __init__() needs no arguments')
        return func(session, Orm, datas)
    return inner
