"""视图函数装饰器，实现将视图函数转为WSGI协议中的application函数"""
from . import views


def application(request_url, request_lines, start_response):
    """
    WSGI协议中的 application ，用于解析并执行视图函数，获取视图函数的返回值并执行 Start_response 函数
    :param request_url:         字符串；请求的url；用于查找对应的视图函数
    :param request_lines:       列表；每个元素为请求头中的一行；
    :param start_response:      函数指针；WSGI 中的一部分，调用以获得响应头
    :return:                    字符串；视图函数的返回值
    """
    for url_tuple in views.urls:
        if request_url in url_tuple:
            view_name, view_func = url_tuple
            print('============ request_lines in application >', request_lines)
            start_response('HTTP/1.1 200 OK', [])
            print("=============== urls >", views.urls)
            return view_func()


