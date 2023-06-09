# -*- coding:utf-8 -*-
# @author xupingmao <578749341@qq.com>
# @since 2020/07/05 17:35:53
# @modified 2022/04/16 08:54:27
from __future__ import print_function

import xutils
import xauth
from xutils import dateutil

def print_debug_info(*args):
    new_args = [dateutil.format_time(), "[stats]"]
    new_args += args
    print(*new_args)

"""统计数据更新的定时任务"""
NOTE_DAO = xutils.DAO("note")

# 衰减单位
DECREMENT = 1

def update_note_index_by_notes(notes):
    for note in notes:
        old_index = note.hot_index or 0
        # 按照线性关系衰退
        new_index = max(old_index - DECREMENT, 0)
        if new_index != old_index:
            print("update hot_index, note_id=%s, old=%s, new=%s" % (note.id, old_index, new_index))
            note.hot_index = new_index
            NOTE_DAO.update_index(note)

class StatsHandler:

    @xauth.login_required("admin")
    def GET(self):
        return u"功能暂时停用"

        user_names = xauth.list_user_names()
        for user_name in user_names:
            notes = NOTE_DAO.list_hot(user_name, 0, -1)
            update_note_index_by_notes(notes)
        return dict(code = "success")

xurls = (
    r"/cron/stats", StatsHandler
)