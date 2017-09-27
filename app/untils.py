#!/usr/bin/env python
# encoding: utf-8
"""
@author: leason
@time: 2017/9/19 10:59
"""
import datetime


# 数据库session提交回滚操作
def operate_commit(fun):
    try:
        fun.commit()
        fun.close()
        return True
    except:
        fun.rollback()
        return False


# 时间格式化
def date_time(day_offset=0, seconds_offset=0, microseconds_offset=0, milliseconds_offset=0, minutes_offset=0,
              hours_offset=0, weeks_offset=0, fmt="%Y-%m-%d %H:%M:%S"):
    """
    获取当前时间
    :param day_offset:
    :param seconds_offset:
    :param microseconds_offset:
    :param milliseconds_offset:
    :param minutes_offset:
    :param hours_offset:
    :param weeks_offset:
    :param fmt: 格式化字符串
    :return:
    """
    _date_time = datetime.datetime.now() + datetime.timedelta(days=day_offset,
                                                              seconds=seconds_offset,
                                                              microseconds=microseconds_offset,
                                                              milliseconds=milliseconds_offset,
                                                              minutes=minutes_offset,
                                                              hours=hours_offset,
                                                              weeks=weeks_offset)
    return _date_time.strftime(fmt)

