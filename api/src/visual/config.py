__author__ = 'Administrator'
import ConfigParser
import os
import redis
import logging
import logging.config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cf = ConfigParser.ConfigParser()
cf.read(BASE_DIR + "/visual/recommend.conf")

rd_host = cf.get("redis", "host")
rd_port = cf.get("redis", "port")
rd_pwd = cf.get("redis", "pwd")
rd = redis.Redis(host=rd_host, port=rd_port, db=0, password=rd_pwd)
