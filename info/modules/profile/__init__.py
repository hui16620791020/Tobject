# 首页模块
from flask import Blueprint

#1. 创建蓝图对象
profile_bp = Blueprint("profile", __name__, url_prefix="/user")

# 切记：让index模块知道有views.py这个文件

from .views import *