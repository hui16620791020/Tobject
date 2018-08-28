# 首页模块
from flask import Blueprint

#1. 创建蓝图对象
news_bp = Blueprint("news", __name__, url_prefix="/news")

# 切记：让index模块知道有views.py这个文件
from .views import *