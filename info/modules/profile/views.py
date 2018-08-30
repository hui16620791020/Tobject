from flask import current_app
from flask import g, jsonify
from flask import request
from flask import session
from info import db
from info.utils.response_code import RET
from . import profile_bp
from flask import render_template
from info.utils.common import login_user_data
from info.utils.image_store import qiniu_image_store
from info import constants

# /user/pic_info  --> GET
@profile_bp.route('/pic_info', methods=["GET", "POST"])
@login_user_data
def pic_info():
    """修改用户头像"""
    # 获取用户对象
    user = g.user

    if request.method == "GET":
        return render_template("news/user_pic_info.html")

    #POST 获取用户提交的头像数据进行修改
    # 1.获取参数
    avatar_data = request.files.get("avatar").read()
    # 2.参数校验
    # 2.1 判断否为空
    if not avatar_data:
        return jsonify(errno=RET.NODATA, errmsg="请上传用户头像")
    if not user:
        return jsonify(errno=RET.SESSIONERR, errmsg="用户未登录")
    #3. 逻辑处理
    try:
        image_name = qiniu_image_store(avatar_data)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg="七牛云上传图片失败")

    # 保存图片名称到user对象的avatar_url属性中
    user.avatar_url = image_name # url域名 + image_name (方便后期更改域名)

    # 保存修改操作到数据库
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="保存图片数据异常")

    #4.返回值处理
    full_url = constants.QINIU_DOMIN_PREFIX + image_name
    data = {
        "avatar_url": full_url
    }
    return jsonify(errno=RET.OK, errmsg="修改用户头像成功", data=data)





# /user/user_info  --> GET
@profile_bp.route('/base_info', methods=["GET", "POST"])
@login_user_data
def base_user_info():
    """返回修改用户基本资料页面"""
    # 获取用户对象
    user = g.user

    if request.method == "GET":
        data = {
            "user_info": user.to_dict() if user else None,
        }
        return render_template("news/user_base_info.html", data=data)

    # POST请求修改用户基本资料
    #1.获取参数
    params_dict = request.json
    nick_name = params_dict.get("nick_name")
    signature = params_dict.get("signature")
    gender = params_dict.get("gender")
    #2.参数校验
    # 2.1 判断否为空
    if not all([nick_name, signature, gender]):
        # 返回错误给前端展示
        return jsonify(errno=RET.PARAMERR, errmsg="提交参数不足")
    if gender not in ["MAN", "WOMAN"]:
        return jsonify(errno=RET.PARAMERR, errmsg="性别数据错误")
    if not user:
        return jsonify(errno=RET.SESSIONERR, errmsg="用户未登录")
    #3.逻辑处理
    user.nick_name = nick_name
    user.signature = signature
    user.gender = gender
    # 注意：修改session数据
    session["nick_name"] = nick_name

    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="修改用户数据异常")

    #4.返回值处理
    return jsonify(errno=RET.OK, errmsg="修改用户数据成功")



# 127.0.0.1:5000/user/info
@profile_bp.route('/info')
@login_user_data
def user_info():
    """用户的基本资料页面"""
    user = g.user
    data = {
        "user_info": user.to_dict() if user else None,
    }
    return render_template("news/user.html", data=data)