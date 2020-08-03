## RUOM

RUOM是一个轻量级的 Web 应用程序框架。

+ 采用 WSGI 协议
+ 几乎完全使用 Python3.8 内置库编写
+ 采用 MVT 架构，支持模板渲染，支持ORM，支持路由分发
+ 可以方便快捷地自定义应用并生成静态界面



----

#### (1) 一个简单的使用样例

##### 1、在 runserver.py  的同级目录下新建你的应用文件夹

以```test_```文件夹为例，此时你的文件结构树应该是这样的：
```
└─RUOM
    │  runserver.py
    ├─conf
    │      _server_config.ini
    ├─RUOM
    │      ...
    └─test_
          __init__.py
```
##### 2、在文件夹中新建一个视图函数文件吧

例如在文件夹中新建一个```test_view.py```视图函数文件：

```python
def test():
    return 'Hello Wrold!'
```

##### 3、将这个应用的视图函数注册到路由表中

打开```RUOM```文件夹下的```urls.py```文件，在下面代码中添加视图函数：

```python
# 路由表
url_list = [
    (r'^/$', init),
]

# 添加 test_view 视图函数
from test_.test_view import test
url_list.append((r'^/test/&', test))
```

##### 4、在配置文件中添加配置项

打开```conf```文件夹中的```_server_config.ini```

```ini
; 服务器配置名
[localtest]
; 服务器ip
ip = 127.0.0.1
; 服务器端口
port = 5551
; 服务器最大连接数
socket_fd = 128
; MySQL数据库ip
db_host = 'localhost'
; MySQL数据库端口
db_port = 3306
; MySQL数据库用户名
db_user = ''
; MySQL数据库密码
db_password = ''
; 数据库名
db_name = ''
; 数据库编码方式
charset = 'utf-8'
```

##### 5、启动服务器！

在终端输入下列命令启动服务器：

```
python3 runservver.py <配置名>
```

在本例中，启动命令为：

```
python3 runserver.py localtest
```

在浏览器中输入```127.0.0.1:5551/test/```就能看到视图函数返回的 Hello World 



----

#### (2) 一个完整项目的结构

一个RUOM应用的完整结构包括：**模型类文件**、**视图函数文件**、**路由文件**、**静态文件夹（模板文件）**；

以```test_```应用为例，完整的文件结构树如下：

```
└─RUOM
    │  runserver.py
    │
    ├─conf
    │      _server_config.ini
    │
    ├─RUOM
    │      app.py
    │      application.py
    │      orm.py
    │      response.py
    │      urls.py
    │      __init__.py
    │
    └─test_
        │  test_model.py
        │  test_view.py
        │  urls.py
        │  __init__.py
        │
        └─templates
                template_test.html
```

各文件作用（按从上至下的顺序）：

+ **runserver.py**    服务器控制模块，用于启动服务器；
+ **conf**    配置文件目录
  + **_server_config.ini**    服务器配置文件；
+ **RUOM**    项目工程文件目录
  + **app.py**    服务器类模块，用于实例化服务器类，对请求进行分发，发送响应数据等；
  + **application.py**    WSGI中的application模块，用于解析并执行视图函数，获取视图函数的返回值并封装为HTTP数据；
  + **orm.py**    模型类基类、元类模块，用于将模型类转为对应的SQL命令；
  + **response.py**     视图函数返回值类模块；
  + **urls.py**    路由模块；
+ <app_name>    应用目录
  + \__init__.py     必须，使得应用变为包便于导入
  + ......    用户自定义模块



----

#### (3) 视图函数

##### 1、按应用配置视图函数路由

在应用文件夹中建立```urls.py```文件，使用列表储存当前应用的路由：

```python
from test_ import test_view

# test_ 应用的路由
urls = [
    (r'^/test/$', test_view.test),
    (r'^/template/$', test_view.template_test),
]
```

将应用路由添加到 RUOM 的路由中，打开 RUOM 目录下的```urls.py```，使用```add_to_urls()```函数添加应用路由到总路由表中：

```python
# 将应用路由添加到路由表的函数
def add_to_urls(app_urls):
    for i in app_urls:
        url_list.append(i)
    return url_list
urls = add_to_urls([])

from test_ import urls as test_urls
urls = add_to_urls(test_urls.urls)
```

##### 2、视图函数的参数

以下面视图函数为例：

```python
# function in ./test_/test_view.py
def test(parameters):
    """测试用视图函数"""
	...
    return parameters
```

该视图函数要接到参数，则需在路由表中进行正则表达式配置：

```python
# list in ./test_/urls.py
urls = [
    ...
    (r'^/test/(.*)$', test_view.test),  # 使用正则表达式接收参数
	...
]
```

##### 3、视图函数的返回值

+ 支持直接返回字符串
+ 支持返回经过渲染的模板文件，详细请看“模板”一节
+ 支持返回 Json 格式字符串（还在开发中......）



----

#### (4) 模型（ORM）

##### 1、模型类的创建

用户模型类需继承于```orm.py```中的```Model```类，例如：

```python
# ./test_/test_model.py
from RUOM.orm import Model

class test_model(Model):
    """测试用模型类"""
	...
```

模型类在初始化时，orm 会自动在数据库中生成相应的表；

##### 2、模型类中字段的定义

用户使用元组储存字段名与字段选项，字段名与每一字段选项使用字符串存储为元组的元素；（注意该元组名并不一定为字段名）。

字段选项应使用 sql 语句语法。（将来可能增加自定义字段类，不必再使用sql语句）

例如：

```python
# ./test_/test_model.py
class test_model(Model):
    name = ('user_name', 'varchar(30)')
    age = ('user_age', 'int unsigned')
    is_delete = ('is_delete', 'boolean')
```

##### 3、模型类的使用

RUOM的模型类使用类似于Django与Flask，可以在视图函数中调用，并获取数据；

在使用时，用户需在视图函数模块中导入要使用的模型类；

例如：

```python
# ./test_/test_model.py
from test_.test_model import test_model

def test(parameters):
    """测试用视图函数"""
    u = test_model()
    u.Insert(name='ALEX', age=18, is_delete=0)
    u.Insert(name='Mercer', age=20, is_delete=1)
    u.Delete(name='ALEX')
    u.Delete(name='Mercer', age=20)
    u.Filter(('age', 'is_delete'), name="ALEX")
    u.Update({'name': "AL", "age": 1, 'is_delete': 0}, name="ALEX")
    return 'Hello world: test view_func'
```

##### 4、模型类中的CURD

+ **插入（Insert）**

  插入数据使用用户模型类的实例对象的```Insert()```函数；

  该函数接收命名参数，参数名需是模型类中定义的字段名（即模型类中字段元组的变量名），必须传入所有属性为非空的参数；

  例如：

  ```python
  u.Insert(name='ALEX', age=18, is_delete=0)
  ```

+ **删除（Delete）**

  删除数据使用用户模型类的实例对象的```Delete()```函数；

  该函数接收命名参数，参数名需是模型类中定义的字段名（即模型类中字段元组的变量名），传入的参数为判断数据的条件；

  例如：

  ```python
  u.Delete(name='Mercer', age=20)
  ```

+ **查找（Filter）**

  删除数据使用用户模型类的实例对象的```Filter()```函数；

  该函数接收的参数有：命名参数，作为查询条件；一个元组，作为查询结果中要返回的字段，元组中的元素为字段名，数据类型为字符串；

  例如：

  ```python
  u.Filter(('age', 'is_delete'), name="ALEX")
  ```

+ **更新（Update）**

  删除数据使用用户模型类的实例对象的```Update()```函数；

  该函数接收的参数有：命名参数，作为查询条件；一个字典，用于更新查找结果中的字段，字典的键值分别为字段名与更新后的值，字段名数据类型为字符串，更新后的值按照字段属性设置；

  例如：

  ```python
  u.Update({'name': "AL", "age": 1, 'is_delete': 0}, name="ALEX")
  ```

##### 5、模型类中的事务

在对模型类进行操作时，并非直接对数据库进行修改吗，而是将 sql 语句存入缓存，用户在误操作后可以回退（暂未支持回退功能）；

因此要对数据库数据作出改变，需要调用用户模型类实例对象的```save()```方法来提交更改；

例如：

```python
u.Insert(name='ALEX', age=18, is_delete=0)
u.save()
```

则数据插入数据库中。



----

#### (5) 模板

##### 1、模板文件的储存

模板文件储存于用户应用目录的一个 template 文件夹内（文件夹名不固定）；

##### 2、模板文件的使用与渲染

用户在视图函数中调用```TemplaterRender()```函数对模板进行渲染，该函数定义在```RUOM.response```模块中；

该函数接收两个参数：其一是模板文件的路径，数据类型为字符串；其二为要进行渲染的模板变量，数据类型为字典，字典的键为模板变量名；

模板渲染实例：

```python
# ./test_/test_view.py
from RUOM.response import TemplateRender

def template_test():
    context = {}
    name = {}
    for i in range(8):
        name[i] = i
    context['name'] = name
    return TemplateRender('RUOM/test_/templates/template_test.html', context)
```

模板文件：

```html
...
<div>{{ name.1 }}</div>
<div>|</div>
<div>{{ name.2 }}</div>
<div>|</div>
<div>{{ name.3 }}</div>
<div>|</div>
<div>{{ name.4 }}</div>
<div>|</div>
<div>{{ name.5 }}</div>
<div>|</div>
<div>{{ name.6 }}</div>
<div>|</div>
<div>{{ name.7 }}</div>
...
```

##### 3、模板语言

+ **模板变量**

  模板变量的书写方式为 <变量名>.<属性>

  当模版引擎遇到"."时，会按照下列顺序解析：

  + 列表的索引值
  + 字典的键
  + 作为类解析，先属性后方法

  例如：

  ```python
  name.0
	# 先检验是否为 name 列表中的第一个元素，即 name[0]
	# 然后检验是否为字典中键为0的值，即name[0]，注意并不会将其转为 name['0']
	# 接着检验其是否属于类，即 name.0 属性与 name.0 方法（注意，属性变量与函数名不能使用数字，此处只是便于举例）
	```

+ **模板标签**

  暂不支持模板标签，未来可能会添加