# 首页模块
from flask import Blueprint

#1. 创建蓝图对象
index_bp = Blueprint("index", __name__, url_prefix="/index")

# 切记：让index模块知道有views.py这个文件
from .views import *