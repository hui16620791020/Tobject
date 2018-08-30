from flask import g

from . import profile_bp
from flask import render_template
from info.utils.common import login_user_data


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