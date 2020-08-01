# from ..RUOM.views import route
from .test_model import test_model
from ..RUOM.response import TemplateRender


#
#
# @route('/test')
def test(parameters):
    """测试用视图函数"""
    u = test_model()
    u.Insert(name='ALEX', age=18, is_delete=0)
    u.Insert(name='Mercer', age=20, is_delete=1)
    u.Delete(name='ALEX')
    u.Delete(name='Mercer', age=20)
    u.Filter(('age', 'is_delete'), name="ALEX")  # 要返回的结果字段以元组传入，查询条件以命名参数传入
    u.Update({'name': "AL", "age": 1, 'is_delete': 0}, name="ALEX")

    print('== test_view.py == func:test == parameters:====>', parameters)

    return 'Hello world: test view_func'


def template_test():
    context = {}
    name = {}
    for i in range(8):
        name[i] = i
    context['name'] = name
    return TemplateRender('RUOM/test_/templates/template_test.html', context)