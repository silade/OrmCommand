#!/usr/bin/env python
# encoding: utf-8
"""
@author: leason
@time: 2017/9/20 16:06
"""


def validate(func):
    def inner(session, Orm, datas):

        pass

        return func(session, Orm, datas)
    return inner
