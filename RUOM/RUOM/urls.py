"""
储存视图函数及路由

使用方法：
    将视图函数添加到路由中即可
"""
from ..test_ import test_view


def init():
    """默认视图函数"""
    return "Hello RUOM"


# 路由
urls = [
    (r'^/$', init),
    (r'^/test/(.*)$', test_view.test)
]


# # 路由装饰器
# def route(url_path):
#     def middle(func):
#         def func_in(*args, **kwargs):
#             urls.append((url_path, func))
#             func(*args, **kwargs)
#
#         return func_in
#
#     return middle

