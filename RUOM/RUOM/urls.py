"""
储存视图函数及路由

使用方法：
    将视图函数添加到路由中即可
"""


def init():
    """默认视图函数"""
    return "Hello RUOM"


# 路由
url_list = [
    (r'^/$', init),
]

# 添加测试用app的路由
from ..test_ import urls as test_urls

for i in test_urls.urls:
    url_list.append(i)
urls = url_list

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
