#!/usr/bin/env python
# encoding: utf-8
"""
@author: leason
@time: 2017/10/19 17:12
"""
import pytest
from ..test import session, ModelBase, db
from ..test import SingleQuery, MultiQuery, SingleInsert, SingleModify, DeleteOne, DeleteSome, QueryOne
from ..test import News, Tag, Type


# content of test_class.py
class TestClass:

    def setup(self):
        """
        初始化数据库
        :return:
        """

        ModelBase.metadata.create_all(bind=db)

        # tag表数据
        tag_add = {
            "tag_name": "123"
        }
        SingleInsert(tag_add).add_method(session, Tag)

        # type表数据
        type_add = {
            "type_name": "123"
        }
        SingleInsert(type_add).add_method(session, Type)

        # news表数据
        item_add = {
            "name": 'leason',
            "des": 123456,
            "type_id": 1,
            "tag_id": 1
        }
        SingleInsert(item_add).add_method(session, News)

    def teardown(self):
        """
        清空数据库
        :return:
        """
        ModelBase.metadata.drop_all(bind=db)

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

    def test_single_query(self):
        """
        单表查询test
        :return:
        """
        cond = {
            "name": "",
            "des": "",
            "create_time": {
                "start_time": "2017-09-19 11:01:21",
                "end_time": "2017-12-26 11:01:22"
            }
        }
        state, sql_total, result = SingleQuery(cond=cond).query_method(session, News)
        assert state is True
        assert sql_total is 1

    def test_multi_query(self):
        """
        多表查询有外键test
        :return:
        """
        cond = {
            "name": "",
            "des": "",
            "create_time": {
                "start_time": "2017-09-19 11:01:21",
                "end_time": "2017-12-26 11:01:22"
            }
        }
        response = {
            "news": [],
            "tag": [],
            "type": []
        }
        state, sql_total, result = MultiQuery(cond=cond, response=response).query_method(session, News, Tag, Type)
        assert state is True
        assert sql_total is 1

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

    def test_delete_some(self):
        """
        批量删除方法test
        :return:
        """
        item_delete = {
            "id": [1]
        }
        result_delete = DeleteSome(item_delete).delete_method(session, News)
        assert result_delete is True

if __name__ == '__main__':
    pytest.main()
