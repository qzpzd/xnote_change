# -*- coding:utf-8 -*-
# @author xupingmao <578749341@qq.com>
# @since 2019/05/18 09:44:13
# @modified 2021/08/14 10:21:56

import xutils
import xmanager
import xauth
from xtemplate import BasePlugin
from xutils import Storage


HTML = r"""
<style>
    .card-body {
        display:none;
    }
</style>

<div class="content-left">
    <div class="card btn-line-height">
        <span>系统一共注册{{event_handler_count}}个事件处理器</span>
    </div>
    
    {% for index, event_type in enumerate(event_type_list) %}
        {% set temp_handler_list = handlers.get(event_type) %}
        <div class="card">
            <div class="card-title">
                <a id="{{event_type}}">{{event_type}}</a>
                <span>({{len(temp_handler_list)}})</span>
                <div class="float-right">
                    <button class="toggle-btn btn-default" data-index="{{index}}" data-toggle="折叠">展开</button>
                </div>
            </div>
            <div class="card-body event-body-{{index}}">
            {% for temp_handler in temp_handler_list %}
                <div class="list-item">{{temp_handler}}</div>
            {% end %}
            </div>
        </div>
    {% end %}
</div>

<div class="content-right">
    <div class="card">
        {% for event_type in event_type_list %}
            <a class="list-item" href="#{{event_type}}">{{event_type}}</a>
        {% end %}
    </div>
</div>

<script>
$(function () {
    $(".toggle-btn").click(function () {
        // 切换展示状态
        var index = $(this).attr("data-index");
        $(".event-body-" + index).toggle();

        // 切换文本
        var text = $(this).text();
        var toggle = $(this).attr("data-toggle");
        $(this).attr("data-toggle", text);
        $(this).text(toggle);
    }); 
});
</script>
"""

class EventHandler(BasePlugin):
    
    title = '系统事件'
    category = "system"
    editable = False
    show_category = False
    
    def handle(self, content):
        self.rows = 0
        self.show_aside = False
        event_type_list = []
        handlers = xmanager._event_manager._handlers
        event_type_list = sorted(handlers.keys())
        
        count = 0
        for key in event_type_list:
            count += len(handlers.get(key))
        
        kw = Storage()
        kw.handlers = handlers
        kw.event_type_list = event_type_list
        kw.event_handler_count = count
        self.writehtml(HTML, **kw)
    
xurls = (
    r"/system/event", EventHandler
)