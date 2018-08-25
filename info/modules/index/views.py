from . import index_bp
from flask import session, current_app, render_template
from info import redis_store, models


#2. 使用蓝图对象
# 127.0.0.1:5000/index/
@index_bp.route('/')
def index():

    # ImportError: cannot import name 'redis_store' 循环导入
    # redis_store.set("name", "laowang")
    # current_app.logger.debug("记录日志")
    # # 没有调整之前： 数据存在在flask后端服务器，只是将session_id使用cookie的方式给了客户端
    # session["name"] = "curry"
    print(current_app.url_map)
    return render_template("index.html")


#返回web的头像图标
@index_bp.route('/favicon.ico')
def favicon():
    """返回项目图标"""
    # send_static_file: 将static中的静态文件发送给浏览器
    return current_app.send_static_file("news/favicon.ico")