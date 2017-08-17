__author__ = 'Administrator'
import ConfigParser
import os
import logging
import logging.config
import redis

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cf = ConfigParser.ConfigParser()
cf.read(BASE_DIR + "/api/recommend.conf")

logging.config.fileConfig(BASE_DIR + "/api/recommend.conf")
logger = logging.getLogger("api")

rd_host = cf.get("redis", "host")
rd_port = cf.get("redis", "port")
rd_pwd = cf.get("redis", "pwd")
rd = redis.Redis(host=rd_host, port=rd_port, db=0, password=rd_pwd)
