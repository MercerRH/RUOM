from RUOM.RUOM.app import RUOM_Server
import sys


def main():
    """控制服务器整体"""
    # python3 runserver.py localtest
    # 参数为要运行的服务器配置
    if not len(sys.argv) == 2:
        print('运行方式为 python3 runserver.py <服务器配置>')
        return

    print("Server Start:")
    app = RUOM_Server(sys.argv[1])
    app.run_forver()


if __name__ == "__main__":
    main()
