"""储存路由"""
from ..test_ import test_view


def init():
    """初始化视图函数"""
    return "Hello RUOM"


urls = [
    ('/', init),
    ('/test', test_view.test)
]
