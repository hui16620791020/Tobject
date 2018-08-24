from flask import Flask, session, current_app
from flask_script import Manager
from info import create_app
import logging


# 单一职责的原则：manage.py 仅仅作为项目启动文件即可
# 工厂方法的调用（ofo公司）
app = create_app("development")

# 7. 创建manager管理类
manager = Manager(app)

if __name__ == '__main__':

    # python manage.py runserver -h -p -d
    # logging.debug("debug的日志信息")
    # logging.info("info的日志信息")
    # logging.warning("warning的日志信息")
    # logging.error("error的日志信息")
    # logging.critical("critical的日志信息")
    #
    # # 在 Flask框架 中，其自己对 Python 的 logging 进行了封装，在 Flask 应用程序中，可以以如下方式进行输出 log:
    # current_app.logger.info("使用flask封住好的方法 info的日志信息")

    manager.run()
