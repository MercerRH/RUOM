"""
储存视图函数及路由

使用方法：
    将视图函数添加到路由中即可
"""


def init():
    """默认视图函数"""
    return "Hello RUOM"


# 路由表
url_list = [
    (r'^/$', init),
]


# 将应用路由添加到路由表的函数
def add_to_urls(app_urls):
    for i in app_urls:
        url_list.append(i)
    return url_list


# 将用于 applications 中的路由表
urls = add_to_urls([])


######## ↓↓↓↓↓↓↓↓↓↓↓↓↓↓在此添加测试用app的路由↓↓↓↓↓↓↓↓↓↓↓↓↓↓
######## ↓↓↓↓↓↓↓↓↓↓↓↓↓↓在此添加测试用app的路由↓↓↓↓↓↓↓↓↓↓↓↓↓↓



from test_ import urls as test_urls
urls = add_to_urls(test_urls.urls)


######## ↑↑↑↑↑↑↑↑↑↑↑↑↑↑在此添加测试用app的路由↑↑↑↑↑↑↑↑↑↑↑↑↑↑
######## ↑↑↑↑↑↑↑↑↑↑↑↑↑↑在此添加测试用app的路由↑↑↑↑↑↑↑↑↑↑↑↑↑↑


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
