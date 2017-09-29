# OrmCommand
基于python flask web项目，对sqlalchemy进一步封装增删改查方法，简化重复操作。适用于通用的增删改查操作，提高效率。

## 目录介绍

- app
  - MysqlCommand
    - Untils
        - untils.py         # 通用方法
    - Validate
        - validate.py       # 校验文件
    - DeleteOne.py          # 删除单条记录
    - MultiQuery.py         # 多表查询
    - SingleQuery.py        # 单表查询
    - SingleModify.py       # 单条记录修改
    - SingleInsert.py       # 单条记录插入
    - QueryOne.py           # 记录详情查询
  - example.py              # 使用示例
  - models.py               # 表models

## 使用说明
