"""模型元类与模型类基类"""
import pymysql


class Model_metaclass(type):
    """
    模型类元类，用于将模型类中的字段进行统合
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
                print("Found Field ===== ", k, ':', v)

        # 删除模型类的类属性
        for k in mappings.keys():
            attrs.pop(k)

        # 在数据库中建表
        sql_conn = pymysql.connect()
        # 获取cursor对象
        cursor = sql_conn.cursor()

        # 将原来的类属性存入一个新的私有属性
        attrs['__mappings__'] = mappings
        attrs['__table__'] = name
        return type.__new__(mcs, name, bases, attrs)


class Model(metaclass=Model_metaclass):
    """
    用户模型类的基类
    """

    def __init__(self):
        pass

    def Insert(self, **kwargs):
        """
        用于生成一个用于将数据插入数据库的类
        该函数返回一个实例对象的引用
        该实例对象具有的方法：
            save()      将数据存入数据库
        """

        class Insert_class(Model):
            def __init__(self, table_name, mappings, **kwargs):
                self.__mappings__ = mappings
                self.__table__ = table_name
                # 将变量储存为实例属性
                for k, v in kwargs.items():
                    print("Found Value ===== ", k, ':', v)
                    setattr(self, k, v)  # 注意！不能使用 self.k = v 来储存

                # 初始化完成后，执行 save() 方法将 sql 语句添加到事务中
                self.save()

            def save(self):
                """将SQL语句添加到事务中"""
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
                print("插入：", sql)  # 测试用

        i = Insert_class(self.__table__, self.__mappings__, **kwargs)
        return i

    def Delete(self, **kwargs):
        class Delete_class(metaclass=Model_metaclass):
            """删除数据"""

            def __init__(self, table_name, mappings, **kwargs):
                self.__mappings__ = mappings
                self.__table__ = table_name
                for k, v in kwargs.items():
                    print("Found Value ===== ", k, ':', v)
                    setattr(self, k, v)  # 注意！不能使用 self.k = v 来储存

                # 初始化完成后，执行 save() 方法将 sql 语句添加到事务中
                self.save()

            def save(self):
                """将SQL语句添加到事务中"""
                field = list()  # 用于格式化sql语句时储存的字段名
                args = list()  # 用于格式化sql语句时储存的数据
                for k, v in self.__mappings__.items():
                    # 并非所有字段都被作为删除条件，因此非删除条件字段不应加到列表中
                    try:
                        field.append(v[0])
                        args.append(getattr(self, k))
                    except AttributeError:
                        continue

                # 将字段与值转化为 字段=值 的形式
                temp = zip(field, args)
                condition_list = list()
                for k, v in temp:
                    # 根据数据类型判断是否添加引号
                    if isinstance(v, str):
                        v = """'%s'""" % v
                    condition_list.append("{}={}".format(k, v))

                # 格式化sql语句
                sql = 'delete from {table_name} where {condition}'.format(table_name=self.__table__,
                                                                          condition=" and ".join(condition_list))
                print(sql)  # 测试用

        d = Delete_class(self.__table__, self.__mappings__, **kwargs)
        return d

    def Filter(self, show_fields, **kwargs):
        """查找数据"""

        class Filter_class(Model):
            def __init__(self, table_name, mappings, show_fields, **kwargs):
                self.__mappings__ = mappings
                self.__table__ = table_name
                self.show_fields = show_fields
                for k, v in kwargs.items():
                    print("Found Value ===== ", k, ':', v)
                    setattr(self, k, v)  # 注意！不能使用 self.k = v 来储存

                # 初始化完成后，执行 save() 方法将 sql 语句添加到事务中
                self.save()

            def save(self):
                """将SQL语句添加到事务中"""
                field = list()  # 用于格式化sql语句时储存的字段名
                args = list()  # 用于格式化sql语句时储存的数据
                for k, v in self.__mappings__.items():
                    # 并非所有字段都被作为判断条件，因此非判断条件字段不应加到列表中
                    try:
                        field.append(v[0])
                        args.append(getattr(self, k))
                    except AttributeError:
                        continue

                # 将字段与值转化为 字段=值 的形式
                temp = zip(field, args)
                condition_list = list()
                for k, v in temp:
                    # 根据数据类型判断是否添加引号
                    if isinstance(v, str):
                        v = """'%s'""" % v
                    condition_list.append("{}={}".format(k, v))

                # 格式化sql语句
                sql = 'select {fields} from {table_name} where {condition}'.format(fields=','.join(self.show_fields),
                                                                                   table_name=self.__table__,
                                                                                   condition=" and ".join(
                                                                                       condition_list))
                print(sql)  # 测试用

        f = Filter_class(self.__table__, self.__mappings__, show_fields, **kwargs)
        return f

    def Update(self, modify_fields, **kwargs):
        """更新数据"""

        class Update_class(Model):
            def __init__(self, table_name, mappings, modify_fields, **kwargs):
                self.__mappings__ = mappings
                self.__table__ = table_name
                self.modify_fields = modify_fields
                # 将变量储存为实例属性
                for k, v in kwargs.items():
                    print("Found Value ===== ", k, ':', v)
                    setattr(self, k, v)  # 注意！不能使用 self.k = v 来储存

                # 初始化完成后，执行 save() 方法将 sql 语句添加到事务中
                self.save()

            def save(self):
                """将SQL语句添加到事务中"""
                field = list()  # 用于格式化sql语句时储存的字段名
                args = list()  # 用于格式化sql语句时储存的数据
                for k, v in self.__mappings__.items():
                    # 并非所有字段都被作为判断条件，因此非判断条件字段不应加到列表中
                    try:
                        field.append(v[0])
                        args.append(getattr(self, k))
                    except AttributeError:
                        continue

                # 查询条件
                condition = zip(field, args)
                condition_list = list()
                for k, v in condition:
                    # 根据数据类型判断是否添加引号
                    if isinstance(v, str):
                        v = """'%s'""" % v
                    condition_list.append("{}={}".format(k, v))
                print(condition_list)

                # 将要修改的字段与值转化为 字段=值 的形式
                modify_fields_list = list()
                for k, v in self.modify_fields.items():
                    # 根据数据类型判断是否添加引号
                    if isinstance(v, str):
                        v = """'%s'""" % v
                    modify_fields_list.append("{}={}".format(k, v))
                print(modify_fields_list)

                # 格式化sql语句
                sql = 'update {table_name} set {f_v} where {condition}'.format(table_name=self.__table__,
                                                                               f_v=','.join(modify_fields_list),
                                                                               condition=' and '.join(condition_list))
                print(sql)  # 测试用

        u = Update_class(self.__table__, self.__mappings__, modify_fields, **kwargs)
        return u



# class test_model(Model):
#     """测试用模型类"""
#     name = ('user_name', 'varchar(30)')  # 使用元组储存字段名与字段类型
#     age = ('user_age', 'int unsigned')  # 字段类型为sql语法
#     is_delete = ('is_delete', 'boolean')


# # 测试语句
# u = test_model()
# u.Insert(name='ALEX', age=18, is_delete=0)
# u.Insert(name='Mercer', age=20, is_delete=1)
# u.Delete(name='ALEX')
# u.Delete(name='Mercer', age=20)
# u.Filter(('age', 'is_delete'), name="ALEX")  # 要返回的结果字段以元组传入，查询条件以命名参数传入
# u.Update({'name':"AL", "age":1, 'is_delete':0}, name="ALEX")
