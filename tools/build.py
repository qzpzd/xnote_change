# -*- coding:utf-8 -*-
# @author mark
# @since 2022/02/19 12:45:23
# @modified 2022/03/12 11:12:08
# @filename build.py
try:
	import termcolor
except ImportError:
	class termcolor:

		@staticmethod
		def colored(text, color):
			return text

def green_text(text):
	return termcolor.colored(text, "green")

def red_text(text):
	return termcolor.colored(text, "red")

class FileBuilder:

	def __init__(self, fpath):
		self.fpath = fpath
		self.fp = open(fpath, "wb")

	def close(self):
		if self.fp != None:
			self.fp.close()
			self.fp = None

	def append(self, fpath):
		print("合并文件:%s ..." % fpath)
		with open(fpath, "rb") as fp:
			buf = fp.read()
			self.fp.write(buf)

	def append_text(self, text):
		self.fp.write(text.encode("utf-8"))

	def __enter__(self):
		return self

	def __exit__(self, type, value, traceback):
		self.close()

def build_app_css():
	print("打包app.build.css ...")
	with FileBuilder("./static/css/app.build.css") as builder:
		builder.append("./static/lib/font-awesome-4.7.0/css/font-awesome.min.css")

		# 通用的css
		builder.append("./static/css/base/reset.css")
		builder.append("./static/css/base/common.css")
		builder.append("./static/css/base/common-icon.css")
		builder.append("./static/css/base/common-tag.css")
		builder.append("./static/css/base/common-layout.css")
		builder.append("./static/css/base/common-button.css")
		builder.append("./static/css/base/common-markdown.css")
		builder.append("./static/css/base/common-dialog.css")
		builder.append("./static/css/base/common-tab.css")
		builder.append("./static/css/base/common-dropdown.css")

		# 场景化的css
		builder.append("./static/css/common-react.css")
		builder.append("./static/css/app.css")
		builder.append("./static/css/message.css")
		builder.append("./static/css/note.css")
		builder.append("./static/css/plugins.css")
		builder.append("./static/css/search.css")
		builder.append("./static/css/todo.css")
		# echo "打包app.build.css ... [OK]"

	print("打包app.build.css %s" % green_text("完成!"))

def build_utils_js():
	print("打包 utils.build.js ...")
	with FileBuilder("./static/js/utils.build.js") as builder:
		# utils.js
		# echo "// generated by build.sh" > ./static/js/utils.build.js
		builder.append_text("/* generated by build.py */\n")
		builder.append("./static/js/base/array.js")
		builder.append("./static/js/base/string.js")
		builder.append("./static/js/base/datetime.js")
		builder.append("./static/js/base/url.js")
		builder.append("./static/js/base/misc.js")
		builder.append("./static/js/base/jq-ext.js")
		# echo "打包utils.build.js ... [OK]"
	print("打包utils.build.js %s" % green_text("完成!"))

def build_app_js():
	print("打包 app.build.js ...")
	with FileBuilder("./static/js/app.build.js") as builder:
		# utils.build.js 也都合并到 app.build.js 文件中
		builder.append("./static/js/utils.build.js")

		# xnote-ui
		builder.append("./static/js/xnote-ui/x-init.js")
		builder.append("./static/js/xnote-ui/x-event.js")
		builder.append("./static/js/xnote-ui/x-ext.js")
		builder.append("./static/js/xnote-ui/core.js")
		builder.append("./static/js/xnote-ui/layer.photos.js")
		builder.append("./static/js/xnote-ui/x-device.js")
		builder.append("./static/js/xnote-ui/x-dropdown.js")
		builder.append("./static/js/xnote-ui/x-photo.js")
		builder.append("./static/js/xnote-ui/x-audio.js")
		builder.append("./static/js/xnote-ui/x-upload.js")
		builder.append("./static/js/xnote-ui/x-dialog.js")
		builder.append("./static/js/xnote-ui/x-tab.js")
		builder.append("./static/js/xnote-ui/x-layout.js")
		builder.append("./static/js/xnote-ui/x-template.js")

		# app.js
		builder.append("./static/js/app.js")
	print("打包 app.build.js %s" % green_text("完成!"))


def main():
	build_app_css()
	print("-"*50)

	build_utils_js()
	print("-"*50)

	build_app_js()
	print("-"*50)

	print(green_text("全部打包完成!"))

if __name__ == '__main__':
	main()
