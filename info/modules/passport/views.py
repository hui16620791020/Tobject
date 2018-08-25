from . import passport_bp
from flask import request, abort, current_app, make_response
from info.utils.captcha.captcha import captcha
from info import redis_store
from info import constants


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
