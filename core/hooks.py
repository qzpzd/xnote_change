# encoding=utf-8
# @author xupingmao
# @since 2023-02-26 23:50:11
# @modified 2022/04/16 18:03:13
from xutils import Storage

def get_search_handler(search_type: str) -> Storage:
    """获取搜索处理器"""
    raise NotImplementedError("待search实现")

def get_category_name_by_code(code) -> str:
    """通过编码获取插件类目名称"""
    raise NotImplementedError("待plugin实现")