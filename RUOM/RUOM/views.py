"""储存视图函数"""
from .urls import urls


# 默认视图函数
def append_to_url(url_path):
    def middle(func):
        def func_in(*args, **kwargs):
            urls.append((url_path, func))
            func(*args, **kwargs)

        return func_in

    return middle

