"""模型元类与模型类基类"""


class Model_metaclass(type):
    """
    模型类元类
    __new__():
        cls     类对象参数
        name    类对象名
        bases   暂不清楚，应该与类的多继承相关
        attrs   类属性
    """

    def __new__(mcs, name, bases, attrs):
        mappings = dict()  # 保存模型类中的字段
        # 判断类属性中属于元组，即判断是否为字段
        for k, v in attrs.items():
            if isinstance(v, tuple):
                mappings[k] = v

        # 删除模型类的类属性
        for k in mappings.keys():
            attrs.pop(k)

        # 将原来的类属性存入一个新的私有属性
        attrs['__mappings__'] = mappings
        attrs['__table__'] = name
        return type.__new__(mcs, name, bases, attrs)


class Model(metaclass=Model_metaclass):
    def __init__(self, **kwargs):
        # 将变量储存为实例属性
        for k, v in kwargs.items():
            setattr(self, k, v)  # 注意！不能使用 self.k = v 来储存

    def save(self):
        field = list()  # 用于格式化sql语句时储存的字段名
        args = list()  # 用于格式化sql语句时储存的数据
        for k, v in self.__mappings__.items():
            field.append(v[0])
            args.append(getattr(self, k, None))

        # 根据数据类型判断是否添加引号
        args_temp = list()
        for _ in args:
            if isinstance(_, int):
                args_temp.append(str(_))
            if isinstance(_, str):
                args_temp.append("""'%s'""" % _)

        # 格式化sql语句
        sql = 'insert into {table_name} ({field}) values ({args})'.format(table_name=self.__table__,
                                                                          field=','.join(field),
                                                                          args=','.join(args_temp))
        print(sql)  # 测试用



