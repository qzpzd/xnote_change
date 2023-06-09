# -*- coding:utf-8 -*-
"""
@Author       : xupingmao
@email        : 578749341@qq.com
@Date         : 2022-08-20 15:46:37
@LastEditors  : xupingmao
@LastEditTime : 2023-03-20 00:11:56
@FilePath     : /xnote/handlers/note/dao_tag.py
@Description  : 标签
"""

import json
import xutils
import handlers.note.dao as note_dao
from xutils import functions
from xutils import dbutil
from xutils import attrget, Storage
from handlers.note.dao_api import NoteDao

tag_bind_db = dbutil.get_table("note_tags")
tag_meta_db = dbutil.get_table("note_tag_meta")
# TODO 可以考虑使用 parent_id 代替 tag_meta.tag_type


class TagBind(Storage):
    """标签绑定信息"""
    def __init__(self):
        self.note_id = ""
        self.user_name = ""
        self.tags = []
        self.parent_id = ""

def dict_to_tag_bind(dict_value):
    if dict_value == None:
        return None
    bind = TagBind()
    bind.update(**dict_value)
    return bind

class TagMeta(Storage):
    """标签元信息"""
    def __init__(self):
        self.user = ""
        self.tag_name = ""
        self.tag_type = "" # group - 笔记本标签 note-笔记标签 global-全局标签(不分区笔记本还是笔记)
        self.amount = 0
        self.book_id = ""
        self.group_id = ""

def get_tags(creator, note_id):
    note_tags = tag_bind_db.get_by_id(note_id, user_name=creator)
    if note_tags:
        return attrget(note_tags, "tags")
    return None


class TagBindDao:
    """标签绑定信息"""

    @staticmethod
    def bind_tag(user_name, note_id, tags, parent_id=None):
        tag_bind_db.update_by_id(note_id, Storage(
            note_id=note_id, user=user_name, tags=tags, parent_id=parent_id))

    @staticmethod
    def get_by_note_id(user_name, note_id):
        record = tag_bind_db.get_by_id(note_id, user_name=user_name)
        return dict_to_tag_bind(record)

    @staticmethod
    def count_user_tag(user_name = "", tag_name = "", parent_id=None):
        assert user_name != ""
        assert tag_name != ""
        
        def filter_func(key, value):
            if tag_name not in value.tags:
                return False
            if parent_id != None and value.parent_id != parent_id:
                return False
            if value.user != user_name:
                return False
            return True
        return tag_bind_db.count_by_func(user_name=user_name, filter_func=filter_func)

    @staticmethod
    def iter_user_tag(user_name, limit=-1):
        for value in tag_bind_db.iter(user_name=user_name, limit=limit):
            yield value


class TagMetaDao:
    """标签元信息"""

    @staticmethod
    def check_tag_type(tag_type):
        assert tag_type in ("group", "global", "note")

    @staticmethod
    def update(tag_info):
        tag_meta_db.update(tag_info)

    @staticmethod
    def delete(tag_info):
        tag_meta_db.delete(tag_info)

    @staticmethod
    def create(tag_info: Storage):
        assert tag_info.user != ""
        assert tag_info.tag_name != ""
        assert tag_info.tag_type != ""
        assert tag_info.amount != None
        tag_meta_db.insert(tag_info)

    @classmethod
    def get_by_name(cls, user_name, tag_name, tag_type="", group_id=None):
        cls.check_tag_type(tag_type)
        result = list_tag_meta(
            user_name, limit=1, tag_type=tag_type, group_id=group_id, tag_name=tag_name)
        if len(result) > 0:
            return result[0]
        return None

    @classmethod
    @xutils.async_func_deco()
    def update_amount_async(cls, user_name: str, tag_names: list, tag_type: str, parent_id=None):
        for tag_name in tag_names:
            tag_info = get_tag_meta_by_name(
                user_name, tag_name, tag_type=tag_type, group_id=parent_id)
            if tag_info != None:
                tag_info.amount = TagBindDao.count_user_tag(
                    user_name, tag_name, parent_id=parent_id)
                cls.update(tag_info)

    @classmethod
    @xutils.async_func_deco()
    def update_global_amount_async(cls, user_name: str, tag_names: list):
        for tag_name in tag_names:
            tag_info = cls.get_by_name(
                user_name = user_name, tag_name = tag_name, tag_type="global")
            amount = TagBindDao.count_user_tag(user_name, tag_name)
            if amount == 0:
                if tag_info == None:
                    return
                else:
                    cls.delete(tag_info)
                return

            if tag_info != None:
                tag_info.amount = amount
                cls.update(tag_info)
            else:
                tag_info = TagMeta()
                tag_info.user = user_name
                tag_info.tag_name = tag_name
                tag_info.tag_type = "global"
                tag_info.amount = amount
                cls.create(tag_info)


def get_tag_meta_by_name(user_name, tag_name, tag_type="group", group_id=None):
    result = list_tag_meta(
        user_name, limit=1, tag_type=tag_type, group_id=group_id, tag_name=tag_name)
    if len(result) > 0:
        return result[0]
    return None


def list_tag_meta(user_name, *, limit=1000, tag_type="group", tag_name=None, group_id=None):
    if tag_type == "note":
        assert group_id != None, "group_id不能为空"

    def list_tag_meta_func(key, value):
        if value.tag_type != tag_type:
            return False
        if tag_name != None and value.tag_name != tag_name:
            return False
        if group_id != None and value.group_id != group_id:
            return False
        return True
    result = tag_meta_db.list(
        limit=limit, filter_func=list_tag_meta_func, user_name=user_name)
    result.sort(key=lambda x: x.amount or 0, reverse=True)
    return result


def count_tag(user_name):
    return tag_meta_db.count_by_user(user_name=user_name)


def bind_tags(creator, note_id, tags, tag_type="group"):
    assert isinstance(tags, list)
    note = note_dao.get_by_id(note_id)
    assert note != None, "笔记不存在"

    old_tag_bind = TagBindDao.get_by_note_id(creator, note_id)

    TagBindDao.bind_tag(creator, note_id, tags, parent_id=note.parent_id)

    note.tags = tags
    note_dao.update_index(note)

    # 老的tag也需要更新
    if old_tag_bind != None:
        for tag in functions.safe_list(old_tag_bind.tags):
            if tag not in tags:
                tags.append(tag)
    TagMetaDao.update_amount_async(
        creator, tags, tag_type, parent_id=note.parent_id)
    TagMetaDao.update_global_amount_async(creator, tags)


update_tags = bind_tags


def delete_tags(creator, note_id):
    tag_bind_db.delete_by_id(note_id, user_name=creator)


def list_by_tag(user, tagname, limit = 1000):
    # TODO 优化查询性能
    if user is None:
        user = "public"

    def list_func(key, value):
        if value.tags is None:
            return False
        return tagname in value.tags

    tags = tag_bind_db.list(filter_func=list_func, user_name=user, limit = limit)
    files = []
    for tag in tags:
        note = note_dao.get_by_id(tag.note_id)
        if note != None:
            files.append(note)
    note_dao.sort_notes(files)
    return files


def batch_get_tags_by_notes(notes):
    result = dict()
    if len(notes) == 0:
        return result

    id_list = []
    for note in notes:
        id_list.append(note.id)

    creator = notes[0].creator
    tags_dict = tag_bind_db.batch_get_by_id(id_list, user_name=creator)

    for note in notes:
        tag_info = tags_dict.get(note.id)
        tags = []
        if tag_info != None and tag_info.tags != None:
            tags = tag_info.tags

        result[note.id] = tags
        note.tags_json = json.dumps(tags)
    return result


class TagInfo(Storage):
    def __init__(self, **kw) -> None:
        self.name = kw.get("name", "")
        self.code = kw.get("code", "")
        self.amount = kw.get("amount", 0)


def list_tag(user):
    if user is None:
        user = "public"

    tags = dict()

    def list_func(key, value):
        if value.tags is None:
            return False
        for tag in value.tags:
            count = tags.get(tag, 0)
            count += 1
            tags[tag] = count

    tag_bind_db.count(filter_func=list_func, user_name=user)

    tag_list = [TagInfo(name=k, amount=tags[k]) for k in tags]
    tag_list.sort(key=lambda x: -x.amount)
    return tag_list


def get_system_tag_list(tag_list=None):
    result = [
        Storage(code="$todo$", name="待办", amount=0),
    ]
    if tag_list != None:
        tag_count_map = dict()
        for item in tag_list:
            tag_count_map[item.name] = item.amount
        for item in result:
            item.amount = tag_count_map.get(item.code, 0)

    return result


def get_system_tag_code_map():
    result = {}
    for item in get_system_tag_list():
        result[item.code] = item.name
    return result


static_code_map = get_system_tag_code_map()

def get_user_defined_tags(tag_list):
    result = []
    for item in tag_list:
        if item.name not in static_code_map:
            result.append(item)
    return result

def get_name_by_code(code):
    return static_code_map.get(code, code)

def handle_tag_for_note(note_info):
    note = note_info
    if note.tags == None:
        note.tags = []
    note.tags_json = xutils.tojson(note.tags)
    tag_info_list = []
    for tag_code in note.tags:
        tag_name = get_name_by_code(tag_code)
        tag_info = Storage(code = tag_code, name = tag_name)
        tag_info.url = "/note/tagname/%s" % xutils.quote(tag_code)

        tag_info_list.append(tag_info)
    note.tag_info_list = tag_info_list

xutils.register_func("note.list_tag", list_tag)
xutils.register_func("note.list_by_tag", list_by_tag)
xutils.register_func("note.get_tags", get_tags)
xutils.register_func("note.update_tags", bind_tags)
xutils.register_func("note_tag_meta.get_by_name", get_tag_meta_by_name)
xutils.register_func("note_tag_meta.list", list_tag_meta)
xutils.register_func("note_tag.get_name_by_code", get_name_by_code)

NoteDao.count_tag = count_tag
