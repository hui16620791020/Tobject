from . import index_bp
from flask import session, current_app
from info import redis_store, models





#2. 使用蓝图对象
# 127.0.0.1:5000/index/
@index_bp.route('/')
def hello_world():

    # ImportError: cannot import name 'redis_store' 循环导入
    redis_store.set("name", "laowang")
    current_app.logger.debug("记录日志")
    # 没有调整之前： 数据存在在flask后端服务器，只是将session_id使用cookie的方式给了客户端
    session["name"] = "curry"
    return 'Hello World! 6666'
