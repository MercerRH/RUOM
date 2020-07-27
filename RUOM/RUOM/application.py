"""视图函数装饰器，实现将视图函数转为WSGI协议中的application函数"""
from . import urls
import re


def application(request_url, request_lines, start_response):
    """
    WSGI协议中的 application ，用于解析并执行视图函数，获取视图函数的返回值并执行 Start_response 函数
    :param request_url:         字符串；请求的url；用于查找对应的视图函数
    :param request_lines:       列表；每个元素为请求头中的一行；
    :param start_response:      函数指针；WSGI 中的一部分，调用以获得响应头
    :return:                    字符串；视图函数的返回值
    """
    for url_tuple in urls.urls:
        re_match = re.match(r'%s' % request_url, url_tuple[0])
        if not re_match:
            view_func = url_tuple[1]
            parameters = re_match.group(1)
            print('============ request_lines in application >', request_lines)
            start_response('HTTP/1.1 200 OK', [])
            print("=============== urls >", urls.urls)
            return view_func(re_match)


