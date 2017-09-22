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
        # 校验Orm 需要有构造方法和to_json方法
        print Orm.__dict__.keys()
        if 'to_json' in Orm.__dict__.keys() and '__init__' in Orm.__dict__.keys():
            pass
        else:
            raise Exception('Orm must have __init__() and to_json()')

        return func(session, Orm, datas)
    return inner
