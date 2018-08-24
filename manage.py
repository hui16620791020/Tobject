from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_wtf.csrf import CSRFProtect
from flask_session import Session


# 创建项目配置类
class Config(object):
    """项目配置类"""

    # 开启debug模式
    DEBUG = True

    # mysql数据库配置
    #数据库链接配置
    SQLALCHEMY_DATABASE_URI = "mysql://root:cq@127.0.0.1:3306/information16"
    # 不跟踪数据库修改
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # redis数据库配置信息
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379
    REDIS_NUM = 6

    # 设置加密字符串
    SECRET_KEY = "/W73UULUS4UFO5omviuVZz6+Bcjs5+2nRdvmyYNq1wEryZsMeluALSDGxGnuYoKX"
    # 调整session存储位置(存储到redis)
    # 指明sesion存储到那种类型的数据库
    SESSION_TYPE = "redis"
    # 上面的指明的数据库的实例对象
    SESSION_REDIS = StrictRedis(host=REDIS_HOST,port=REDIS_PORT,db=REDIS_NUM)
    # session数据需要加密
    SESSION_USE_SIGNER = True
    # 不设置永久存储
    SESSION_PERMANENT = False
    # 默认存储的有效时长 （没有调整之前默认值是timedelta(days=31)）
    PERMANENT_SESSION_LIFETIME = 86400 * 2




# 1.创建app对象
app = Flask(__name__)
# 2.注册配置信息到app对象
app.config.from_object(Config)
# 3. 创建mysql数据库对象
db = SQLAlchemy(app)
# 4. 创建redis数据库对象
redis_store = StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=Config.REDIS_NUM)
# 5. 开启csrf后端保护验证机制
# 提取cookie中的csrf_token和ajax请求头里面csrf_token进行比较验证操作
csrf = CSRFProtect(app)
# 6.创建session拓展类的对象(将session的存储调整到redis中)
Session(app)




@app.route('/')
def hello_world():
    # 没有调整之前： 数据存在在flask后端服务器，只是将session_id使用cookie的方式给了客户端
    session["name"] = "curry"

    return 'Hello World! 6666'


if __name__ == '__main__':
    app.run(debug=True)
