# encoding=utf-8
# Created by xupingmao on 2017/05/23
# @modified 2019/12/08 15:00:26

import sys
import os
sys.path.insert(1, "lib")
sys.path.insert(1, "core")
import unittest
import json
import web
import six
import xmanager
import xutils
import xtemplate
import xconfig
import xtables
from xutils import u, dbutil

# cannot perform relative import
try:
    import test_base
except ImportError:
    from tests import test_base

app          = test_base.init()
json_request = test_base.json_request
request_html = test_base.request_html
BaseTestCase = test_base.BaseTestCase

def get_script_path(name):
    return os.path.join(xconfig.SCRIPTS_DIR, name)

class TextPage(xtemplate.BaseTextPlugin):

    def get_input(self):
        return ""

    def get_format(self):
        return ""

    def handle(self, input):
        return "test"

class TestMain(BaseTestCase):

    def test_message_create(self):
        # Py2: webpy会自动把str对象转成unicode对象，data参数传unicode反而会有问题
        response = json_request("/message/save", method="POST", data=dict(content="Xnote-Unit-Test"))
        self.assertEqual("success", response.get("code"))
        data = response.get("data")
        # Py2: 判断的时候必须使用unicode
        self.assertEqual(u"Xnote-Unit-Test", data.get("content"))
        json_request("/message/touch", method="POST", data=dict(id=data.get("id")))
        json_request("/message/delete", method="POST", data=dict(id=data.get("id")))

    def test_message_list(self):
        json_request("/message/list")
        json_request("/message/list?status=created")
        json_request("/message/list?status=suspended")
        # search
        json_request("/message/list?key=1")

    def test_message_finish(self):
        response = json_request("/message/save", method="POST", data=dict(content="Xnote-Unit-Test", tag="task"))
        self.assertEqual("success", response.get("code"))
        data = response.get("data")
        msg_id = data['id']

        json_request("/message/finish", method="POST", data=dict(id = msg_id))
        done_result = json_request("/message/list?tag=done")

        self.assertEqual("success", done_result['code'])

        done_list = done_result['data']
        self.assertEqual(2, len(done_list))

        for msg in done_list:
            json_request("/message/delete", method="POST", data=dict(id = msg['id']))



