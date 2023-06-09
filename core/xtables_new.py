# -*- coding:utf-8 -*-
"""
@Author       : xupingmao
@email        : 578749341@qq.com
@Date         : 2021/12/27 23:34:03
@LastEditors  : xupingmao
@LastEditTime : 2023-03-25 15:27:56
@FilePath     : /xnote/core/xtables_new.py
@Description  : 数据库-表定义
"""

import xutils
from xutils import dbutil

@xutils.log_init_deco("xtables_new")
def init():
    # 使用NoSQL风格的数据库接口
    # 数据库索引保证最终一致，不保证强一致
    dbutil.register_table("sys_log", "系统日志")
    dbutil.register_table("dict", "词典")

    init_note_tables()
    init_message_tables()
    # 初始化一些废弃的表，防止覆盖老版本数据
    init_old_table()


    # 文件相关
    db = dbutil.register_table("fs_index", "文件索引")
    db.register_index("ftype", comment = "类型索引")
    # 网络文件映射到本地文件
    dbutil.register_table("fs_map", "文件映射")
    dbutil.register_table("fs_ctype", "缓存的Content-Type")
    dbutil.register_table("txt_info", "txt文件信息")

    # 用户信息
    dbutil.register_table("user", "用户信息表")
    dbutil.register_table("user_config", "用户配置表")
    db = dbutil.register_table("session", "用户会话信息")
    db.register_index("user", columns=["user_name"])
    
    dbutil.register_table("user_stat", "用户数据统计")

    db = dbutil.register_table("plugin_visit", "插件访问日志")
    db.register_index("uk_url", columns=["user", "url"])

    # 月度计划
    db = dbutil.register_table("month_plan", "月度计划")
    db.register_index("user_month", columns = ["user", "month"])

    # uv统计
    db = dbutil.register_table("uv", "uv访问统计")
    db.register_index("date_ip", columns = ["date", "ip"])

    # 重建索引(系统会根据索引版本增量构建)
    rebuild_index()

def init_old_table():
    # 统计数据
    db = dbutil.register_table("plugin_visit_log", "插件访问日志", user_attr="user", check_user = True)
    db.register_index("url", comment = "页面URL")
    db.is_deleted = True

    db = dbutil.register_table("user_session_rel", "用户会话关系")
    db.is_deleted = True

    db = dbutil.register_table("note_skey", "用户维度的skey索引 <note_skey:user:skey>")
    db.is_deleted = True

    db = dbutil.register_table("msg_task_idx", "待办索引")
    db.is_deleted = True

def init_note_tables():
    # 笔记信息
    dbutil.register_table("note_tags", "笔记标签绑定",
                          category="note", user_attr="user")
    dbutil.register_table("note_tag_meta", "笔记标签",
                          category="note", user_attr="user")
    dbutil.register_table("note_draft", "笔记草稿", category="note")
    dbutil.register_table("note_lock", "笔记编辑锁", category="note")

    dbutil.register_table("note_full", "笔记的完整信息")

    # ID维度笔记索引
    db = dbutil.register_table(
        "note_index", "笔记索引，不包含内容", category="note")
    db.register_index("parent_id", comment = "父级笔记ID")
    db.register_index("name", columns=["creator", "name"])
    db.register_index("ctime", columns=["creator", "ctime"])
    db.register_index("skey", columns=["creator", "skey"])

    # 用户维度笔记索引
    db = dbutil.register_table("note_tiny", "用户维度的笔记索引",
                               category="note", check_user=True, user_attr="creator")
    db.register_index("name")
    db.register_index("ctime")
    db.register_index("parent_id")

    # 笔记修改历史
    dbutil.register_table("note_history_index", "笔记历史索引", category="note")
    db = dbutil.register_table("search_history", "搜索历史", user_attr="user", check_user=True)
    db.drop_index("user", comment = "使用二级key的表,不需要user索引")

    # 分享关系
    db = dbutil.register_table("note_share", "笔记分享", category="note")
    db.register_index("note_id", comment = "笔记ID")
    db.register_index("to_user", comment = "分享的目标用户")


    db = dbutil.register_table("comment", "评论模型", category="note")
    db.register_index("user", comment = "用户索引", index_type="copy")
    db.register_index("note_id", comment = "笔记ID索引", index_type="copy")


    # 公共笔记
    db = dbutil.register_table("note_public", "公共笔记", category="note")
    db.register_index("hot_index")
    db.register_index("share_time")

    # 操作日志
    db = dbutil.register_table("user_note_log", "用户笔记操作日志", check_user=True, user_attr="user")
    db.register_index("visit_cnt")
    db.register_index("atime")
    db.register_index("mtime")
    db.register_index("ctime")


def init_message_tables():
    db = dbutil.register_table("message", "短文本", check_user=True, user_attr="user")
    db.register_index("date")
    db.register_index("tag")
    db.register_index("tag_ctime", columns=["tag", "ctime"])
    db.register_index("ctime")

    db = dbutil.register_table("msg_key", "备忘关键字/标签", check_user=True, user_attr="user")
    dbutil.register_table("msg_search_history", "备忘搜索历史", check_user=True, user_attr="user")
    dbutil.register_table("msg_history", "备忘历史")


def rebuild_index():
    dbutil.get_table("note_index").rebuild_index("v5")
    dbutil.get_table("note_tiny").rebuild_index("v3")
    dbutil.get_table("plugin_visit_log").rebuild_index("v2")
    dbutil.get_table("note_public").rebuild_index("v1")
    dbutil.get_table("comment").rebuild_index("v1")
    dbutil.get_table("uv").rebuild_index("v1")
    dbutil.get_table("user_note_log").rebuild_index("v1")
    dbutil.get_table("message").rebuild_index("v2")
    dbutil.get_table("note_share").rebuild_index("v1")
