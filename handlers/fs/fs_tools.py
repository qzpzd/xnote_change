# -*- coding:utf-8 -*-
# @author xupingmao <578749341@qq.com>
# @since 2020/12/08 01:46:35
# @modified 2021/07/04 17:09:54
# -*- coding:utf-8 -*-
# @since 2018-11-22 00:46:26
import os
import re
import math
import time
import web
import xconfig
import xutils
import xauth
import xmanager
import xtables
import random
from xutils import cacheutil
from xutils.htmlutil import *
from xutils import dbutil
from xtemplate import BasePlugin

HEADER = """
<!-- 插件头部 -->
<div class="card">
    <div class="grid-title btn-line-height">
        <span>{{plugin.title}}</span>
        <div class="float-right">
            <a class="btn btn-default" href="/fs_list">收藏夹</a>
            <a class="btn btn-default" href="/fs_tools">工具</a>
        </div>
    </div>
</div>

{% include plugin/header/plugin_category.html %}
"""

HTML = '''
<div class="card">
{% for note in notes %}
    <a class="list-link" href="{{note.url}}">
        <span>{{note.title}}</span>
        <div class="float-right">
            {% if note.visit_cnt != None %}
                <i class="fa fa-eye-o"></i>
                <span class="plugin-right-span">热度: {{note.visit_cnt}}</span>
            {% end %}
            <i class="fa fa-chevron-right"></i>
        </div>
    </a>
{% end %}
</div>
'''


class Main(BasePlugin):

    title = u"文件工具"
    category = "dir"
    rows = 0
    editable = False

    def handle(self, input):
        user  = xauth.current_name()
        notes = xmanager.find_plugins("dir")

        xmanager.add_visit_log(user, "/fs_tools")
        self.writeheader(HEADER, plugin = self, plugin_category = "dir")
        self.writetemplate(HTML, notes = notes)
        

xurls = (
    r"/fs_tools", Main
)
