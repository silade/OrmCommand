#!/usr/bin/env python
# encoding: utf-8
"""
@author: leason
@time: 2017/10/19 17:12
"""
import pytest
from ..test import *

# content of test_class.py
class TestClass:

    def setup(self):

        ModelBase.metadata.create_all(bind=db)
        item_add = {
            "name": 'leason',
            "des": 123456
        }
        SingleInsert(item_add).add_method(session, News)

    def test_add(self):
        """
        添加方法test
        :return:
        """
        item_add = {
            "name": 'leason',
            "des": 123456
        }
        result_add = SingleInsert(item_add).add_method(session, News)
        assert result_add is True

    def test_modify(self):
        """
        编辑方法test
        :return:
        """
        data = {
            "primary_key": {
                "id": 1
            },
            "items": {
                "name": "llx",
                "des": 845
            }
        }
        result_modify = SingleModify(data['primary_key'], data['items']).modify_method(session, News)
        assert result_modify is True

    def test_delete(self):
        """
        删除方法test
        :return:
        """
        item_delete = {
            "id": 1
        }
        result_delete = DeleteOne(item_delete).delete_method(session, News)
        assert result_delete is True

if __name__ == '__main__':
    pytest.main()
