from flask import render_template
from . import news_bp


# 127.0.0.1:5000/news/12
# 点击那条新闻需要将改新闻的id传过来方便查询
@news_bp.route('/<int:news_id>')
def news_detail(news_id):
    """新闻详情首页接口"""
    data = {}
    return render_template("news/detail.html", data=data)