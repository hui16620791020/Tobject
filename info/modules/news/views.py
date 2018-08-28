from flask import abort, jsonify
from flask import current_app
from flask import g
from flask import render_template
from flask import request
from flask import session
from info import constants, db
from info.models import News, User
from info.utils.response_code import RET
from . import news_bp
from info.utils.common import login_user_data


# /news/news_collect POST
@news_bp.route('/news_collect', methods=["POST"])
@login_user_data
def news_collect():
    """新闻收藏、取消收藏接口"""
    """
    1.获取参数
        1.1 用户对象 新闻id action(收藏、取消收藏)
    2.校验参数
        2.1 非空判断
        2.2 action处于["collect", "cancel_collect"]
    3.逻辑处理
        3.1 根据新闻id查询出该新闻
        3.2 收藏：将新闻添加到user.collection_news列表中
        3.3 取消收藏：将新闻从user.collection_news列表移除
    4.返回值处理
    """

    # 1.1 用户对象 新闻id action(收藏、取消收藏)
    params_dict = request.json
    news_id = params_dict.get("news_id")
    action = params_dict.get("action")
    user = g.user

    #2.1 非空判断
    if not all([news_id, action, user]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不足")
    #2.2 action处于["collect", "cancel_collect"]
    if action not in ["collect", "cancel_collect"]:
        return jsonify(errno=RET.PARAMERR, errmsg="参数填写错误")

    #3.1 根据新闻id查询出该新闻
    news = None
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询新闻数据异常")

    if not news:
        return jsonify(errno=RET.NODATA, errmsg="新闻不存在")

    #3.2 收藏：将新闻添加到user.collection_news列表中
    if action == "collect":
        user.collection_news.append(news)
    else:
        #3.3 取消收藏：将新闻从user.collection_news列表移除
        user.collection_news.remove(news)

    # 4.返回值处理
    return jsonify(errno=RET.OK, errmsg="OK")


# 127.0.0.1:5000/news/12
# 点击那条新闻需要将改新闻的id传过来方便查询
@news_bp.route('/<int:news_id>')
@login_user_data
def news_detail(news_id):
    """新闻详情首页接口"""
    # ------- 1.查询用户信息将用户信息通过模板带回进行展示--------
    user = g.user

    # 1. 如果用户登录成功就能够获取用户的id
    # user_id = session.get("user_id")
    # user = None
    # # 2. 根据用户id查询用户所有的数据
    # try:
    #     if user_id:
    #         user = User.query.get(user_id)
    # except Exception as e:
    #     current_app.logger.error(e)
        # 切记不需要return

    # if user:
    #     return user.to_dict()
    # else:
    #     return None
    # 3.经用户模型对象转换成用户的字典对象

    # ------- 2.查询新闻的点击排行数据进行展示--------
    try:
        news_model_list = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS)
    except Exception as e:
        current_app.logger.error(e)

    # 将模型列表转换成字典列表
    news_dict_list = []
    for news in news_model_list if news_model_list else []:
        # 将新闻模型对象转成成字典对象添加到news_dict_list列表中
        news_dict_list.append(news.to_dict())

    # ------- 3.查询新闻的详情内容数据进行展示--------
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
        abort(404)

    if not news:
        abort(404)

    # 注意： 浏览量自增
    news.clicks += 1

    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        # 回滚
        db.session.rollback()
        abort(404)

    # ------- 4.查询用户是否收藏过该新闻--------
    # False: 未收藏 True: 收藏过了
    is_collected = False

    # 1.判断用户是否登录
    if not user:
        abort(404)

    # 2.判断新闻对象是否在收藏列表
    if news in user.collection_news:
        # 已经收藏了该新闻
        is_collected = True


    # 组织响应数据
    data = {
        "user_info": user.to_dict() if user else None,
        "newsClicksList": news_dict_list,
        "news": news.to_dict() if news else None,
        "is_collected": is_collected
    }

    return render_template("news/detail.html", data=data)