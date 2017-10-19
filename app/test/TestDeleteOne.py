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

    def test_one(self):

        item = {
            "name": 'leason',
            "des": 123456
        }
        result = SingleInsert(item).add_method(session, News)
        assert result is True

if __name__ == '__main__':
    pytest.main()
