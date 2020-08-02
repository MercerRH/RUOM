from RUOM.orm import Model


class test_model(Model):
    """测试用模型类"""
    name = ('user_name', 'varchar(30)')  # 使用元组储存字段名与字段类型
    age = ('user_age', 'int unsigned')  # 字段类型为sql语法
    is_delete = ('is_delete', 'boolean')