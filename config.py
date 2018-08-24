from redis import StrictRedis
import logging


# 创建项目配置类
class Config(object):
    """项目配置父类"""

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


class DevelopmentConfig(Config):
    """开发阶段的项目配置"""
    # 开启debug模式
    DEBUG = True
    # 设置日志级别
    LOG_LEVEL = logging.DEBUG


class ProductionConfig(Config):
    """生产阶段的项目配置"""
    # 开启debug模式
    DEBUG = False
    # 设置日志级别
    LOG_LEVEL = logging.WARNING
    # 修改数据库的链接对象
    # 数据库链接配置
    # SQLALCHEMY_DATABASE_URI = "mysql://root:cq@服务器ip地址:3306/information16"


# 使用方式： config_dict["development"]
# 暴露一个借口给外界调用
config_dict ={
    "development": DevelopmentConfig,
    "production": ProductionConfig
}