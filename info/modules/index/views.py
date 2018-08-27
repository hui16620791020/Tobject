from info.models import User, News
from . import index_bp
from flask import session, current_app, render_template
from info import redis_store, models, constants


#2. 使用蓝图对象
# 127.0.0.1:5000/index/
@index_bp.route('/')
def index():
    #------- 1.查询用户信息将用户信息通过模板带回进行展示--------
    # 1. 如果用户登录成功就能够获取用户的id
    user_id = session.get("user_id")
    user = None
    # 2. 根据用户id查询用户所有的数据
    try:
        if user_id:
            user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        # 切记不需要return

    # if user:
    #     return user.to_dict()
    # else:
    #     return None
    # 3.经用户模型对象转换成用户的字典对象

    #------- 2.查询新闻的点击排行数据进行展示--------
    try:
        news_model_list = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS)
    except Exception as e:
        current_app.logger.error(e)

    # 将模型列表转换成字典列表
    news_dict_list = []
    for news in news_model_list if news_model_list else []:
        # 将新闻模型对象转成成字典对象添加到news_dict_list列表中
        news_dict_list.append(news.to_dict())

    # 构建响应数据
    data = {
        "user_info": user.to_dict() if user else None,
        "newsClicksList": news_dict_list
    }

    return render_template("index.html", data=data)


#返回web的头像图标
@index_bp.route('/favicon.ico')
def favicon():
    """返回项目图标"""
    # send_static_file: 将static中的静态文件发送给浏览器
    return current_app.send_static_file("news/favicon.ico")