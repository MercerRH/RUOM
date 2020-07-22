# from ..RUOM.views import route
from .test_model import test_model


#
#
# @route('/test')
def test():
    """测试用视图函数"""
    u = test_model(name='ALEX', age=18, is_delete=0)
    u.save()
    return 'Hello world: test view_func'
