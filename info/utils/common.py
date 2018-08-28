from flask import current_app, g
from flask import session
import functools



def do_index_class(index):
    """对传入的index下标返回不同class属性值"""
    if index == 1:
        return "first"
    elif index == 2:
        return "second"
    elif index == 3:
        return "third"
    else:
        return ""


# 将视图函数添加上该装饰器，就能获取到用户对象
def login_user_data(view_func):

    # 防止内层装饰器修改被装饰的函数的名字
    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):

        # 需求：
        # 获取session里面uers_id
        user_id = session.get("user_id")
        # 根据user_id查询用户数据
        user = None
        # 2. 根据用户id查询用户所有的数据
        try:
            # 延迟导入 解决循环导入问题
            from info.models import User
            if user_id:
                user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)
        # 3.保存数据后在view_func函数中能够获取到用户数据(*******)
        g.user = user
        # 在进入实现函数里面由于是处于同一个request请求，里面就能够获取g对象中的临时变量
        result = view_func(*args, **kwargs)
        return result
    return wrapper



# @login_user_data
# def news_detail(news_id):
#     """新闻详情首页接口"""
#     # ------- 1.查询用户信息将用户信息通过模板带回进行展示--------
#     user = g.user