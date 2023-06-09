# -*- coding:utf-8 -*-
"""
@Author       : xupingmao
@email        : 578749341@qq.com
@Date         : 2023-04-15 14:39:26
@LastEditors  : xupingmao
@LastEditTime : 2023-04-15 15:38:19
@FilePath     : /xnote/handlers/dict/dict_dao.py
@Description  : 描述
"""
import xtables
from xutils import Storage

class DictItem(Storage):

    def __init__(self):
        self.key = ""
        self.value = ""
        self.ctime = ""
        self.mtime = ""

def dict_to_obj(item):
    if item == None:
        return None
    result = DictItem()
    result.update(item)
    return result

def get_by_id(id):
    table = xtables.get_dict_table()
    item = table.select_first(where=dict(id=id))
    return dict_to_obj(item)


def update(id, value):
    assert isinstance(id, int), "id必须为数字"
    table = xtables.get_dict_table()
    return table.update(value = value, where = dict(id = id))

def delete(id):
    table = xtables.get_dict_table()
    return table.delete(where = dict(id = id))

