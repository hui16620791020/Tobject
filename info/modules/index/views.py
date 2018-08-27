from info.models import User
from . import index_bp
from flask import session, current_app, render_template
from info import redis_store, models


#2. 使用蓝图对象
# 127.0.0.1:5000/index/
@index_bp.route('/')
def index():
    #  查询用户信息将用户信息通过模板带回进行展示
    # 1. 如果用户登录成功就能够获取用户的id
    user_id = session.get("user_id")
    # 2. 根据用户id查询用户所有的数据
    if user_id:
        user = User.query.get(user_id)

    # if user:
    #     return user.to_dict()
    # else:
    #     return None
    # 3.经用户模型对象转换成用户的字典对象
    data = {
        "user_info": user.to_dict() if user else None
    }

    return render_template("index.html", data=data)


#返回web的头像图标
@index_bp.route('/favicon.ico')
def favicon():
    """返回项目图标"""
    # send_static_file: 将static中的静态文件发送给浏览器
    return current_app.send_static_file("news/favicon.ico")