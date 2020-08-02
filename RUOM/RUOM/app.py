import logging

logging.basicConfig(level=logging.INFO)

# import gevent
import threading
import socket
import re
import configparser

# from gevent import monkey
#
# # 修补
# monkey.patch_all()

from .application import application


class RUOM_Server(object):
    """
    RUOM服务器类
    各函数功能：
        run_forever:     运行服务器，与客户端建立连接并为每个客户端创建相应的线程
        client_handle:   对客户端请求进行解析，进行路由分发，并发送响应数据
    """

    def __init__(self, server_conf):
        # 读取配置文件信息
        config = configparser.ConfigParser()
        config.read("RUOM/conf/_server_config.ini", encoding='utf-8')
        server = (config[server_conf]['ip'], int(config[server_conf]['port']))  # 服务器信息

        # 创建套接字
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置端口复用
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 绑定本地信息
        self.s.bind(server)
        # 变为监听套接字，最大连接数为128
        self.s.listen(int(config[server_conf]['socket_fd']))

    def run_forever(self):
        """运行服务器"""
        while True:
            # 等待连接请求
            cli_socket, cli_addr = self.s.accept()
            cli_cls = Client()
            # # 使用协程分别对各个连接进行处理
            # gevent.spawn(self.client_handle, cli_socket, cli_cls)
            # 使用线程分别对各个连接进行处理
            t = threading.Thread(target=self.client_handle, args=(cli_socket, cli_cls))
            t.start()

    def client_handle(self, client_socket, cli_cls):
        """
        对客户端请求进行处理，对请求的资源进行判断、分发
        接收的参数为客户端套接字
        """
        # while True:
        # 接收数据
        cli_request = client_socket.recv(1024).decode('utf-8')

        # # 客户端关闭套接字时关闭本套接字
        # if not cli_request:
        #     client_socket.close()
        #     break

        # 对收到的请求数据进行处理
        cli_request_lines = cli_request.splitlines()
        request_url = re.match(r'.*\s(.*)\s.*', cli_request_lines[0]).group(1)

        # 对请求进行分发
        response_body = application(request_url, cli_request_lines, cli_cls.start_response)
        response_head = cli_cls.response_head
        response_data = response_head + '\r\n\r\n' + response_body + '\n'

        # 发送响应数据
        client_socket.send(response_data.encode('utf-8'))
        print("== app.py == cls:RUOM_Server == func:client_handle == 数据发送成功 ==>")
        client_socket.close()


class Client(object):
    """对每个客户端套接字分别进行处理"""

    def __init__(self):
        self.response_head = ''

    def start_response(self, resp_first_line, resp_head):
        """
        start_response(self, resp_first_line, resp_head)
        接收视图函数返回的请求头并将其拼接，并将其赋给
        参数详情：
            resp_first_line    字符串；为响应状态行；例如 'HTTP/1.1 200 OK'
            resp_head          列表；每项元素为含有两个字符串的元组，这两个元素分别为响应头中的键值对，例如 [('ContentType', 'text/HTML')]
        """
        self.response_head += resp_first_line
        for key, val in resp_head:
            self.response_head += '\r\n' + key + ':' + val
