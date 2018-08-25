from . import passport_bp
from flask import request, abort, current_app, make_response, jsonify
from info.utils.captcha.captcha import captcha
from info import redis_store
from info.utils.response_code import RET
from info import constants
import re
from info.models import User
from info.lib.yuntongxun.sms import CCP
import json
import random

# /passport/sms_code
@passport_bp.route('/sms_code', methods=["POST"])
def send_sms():
    """点击发送短信验证码接口"""
    """
    1.获取参数
        1.1 手机号码，用户填写的图片验证码真实值，编号
    2.校验参数
        2.1 判断 手机号码，用户填写的图片验证码真实值，编号是否为空
        2.2 手机号码格式校验
    3.逻辑处理
        3.1 根据编号去获取redis中存储的图片验证码真实值
            3.1.1 image_code_id有值，删除
            3.1.2 image_code_id没有值，表示编号过期
        3.2 对比用户填写的真实值和后端获取的验证码真实值是否一致
        一致：发送短信验证码
        不一致：验证码填写错误
        3.3 保存短信验证码到redis
    4.返回值处理
    """
    #1.获取参数（json类型参数）
    #1.1 手机号码，用户填写的图片验证码真实值，编号
    #request.json 获取到数据会自动转换成python对象（dict or list）
    param_dict = request.json
    mobile = param_dict.get("mobile")
    image_code = param_dict.get("image_code")
    image_code_id = param_dict.get("image_code_id")

    #2.校验参数
    #2.1 判断 手机号码，用户填写的图片验证码真实值，编号是否为空
    if not all([mobile, image_code, image_code_id]):
        # 返回错误给前端展示
        return jsonify(errno=RET.PARAMERR, errmsg="提交参数不足")
    #2.2 手机号码格式校验
    if not re.match('1[3578][0-9]{9}', mobile):
        return jsonify(errno=RET.PARAMERR, errmsg="手机号码格式错误")

    # 3.逻辑处理
    try:
        #3.1 根据编号去获取redis中存储的图片验证码真实值
        real_image_code = redis_store.get("imagecode_%s" %image_code_id)
        # 3.1.1 image_code_id有值，删除 防止下次多次使用同一个real_image_code来访问
        if real_image_code:
            redis_store.delete(real_image_code)
    except Exception as e:
        # 记录日志
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg="查询图片验证码异常")

    #3.1.2 image_code_id没有值，表示编号过期
    if not real_image_code:
        return jsonify(errno=RET.NODATA, errmsg="验证码真实值过期")

    #3.2 对比用户填写的真实值和后端获取的验证码真实值是否一致
    if image_code.lower() != real_image_code.lower():
        return jsonify(errno=RET.DATAERR, errmsg="图片验证码填写错误")

    # 一致：发送短信验证码
    # 查看手机号码是否注册过
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        return jsonify(errno=RET.DATAERR, errmsg="查询用户手机号码是否存在异常")
    # 已经注册过了
    if user:
        return jsonify(errno=RET.DATAEXIST, errmsg="用户已经注册过")

    #1. 生成短信验证码随机值
    sms_code = random.randint(0, 999999)
    sms_code = "%06d" %sms_code
    #2. 调用云通讯发送短信验证码
    result = CCP().send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES/60], 1)
    # 发送短信验证码失败
    if result != 0:
        return jsonify(errno=RET.THIRDERR, errmsg="发送短信验证码失败")

    #3.发送短信验证码成功
    try:
        redis_store.set("SMS_%s" %mobile, sms_code, ex=constants.SMS_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="存储短信验证码真实值失败")

    # 返回值处理
    return jsonify(errno=RET.OK, errmsg="发送短信验证码成功，请注意查收")


# 127.0.0.1:5000/passport/image_code?imageCodeId=编号
@passport_bp.route('/image_code')
def get_imagecode():
    """
    图片验证码的后端接口(GET)
    1. 获取参数
        1.1 获取前端携带的imageCodeId编号
    2. 校验参数
        2.1 imageCodeId编号是否有值
    3. 逻辑处理
        3.0 生成验证码图片&验证码图片的真实值
        3.1 使用imageCodeId编号作为key存储生成的图片验证码真实值
    4. 返回值处理
        4.1 返回生成的图片
    """
    # 1. 获取参数
    # 1.1 获取前端携带的imageCodeId编号
    imageCodeId = request.args.get("imageCodeId")

    #2. 校验参数
    #2.1 imageCodeId编号是否有值
    if not imageCodeId:
        abort(404)
    #3. 逻辑处理
    #3.0 生成验证码图片&验证码图片的真实值
    name, text, image = captcha.generate_captcha()

    try:
        #3.1 使用imageCodeId编号作为key存储生成的图片验证码真实值
        redis_store.set("imagecode_%s" %imageCodeId, text, ex=constants.IMAGE_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        abort(500)

    #4. 返回值处理
    #4.1 返回生成的图片
    respose = make_response(image)
    respose.headers["Content-Type"] = "image/jpg"
    return respose
