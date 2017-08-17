# -*- coding: utf-8 -*-
from datetime import datetime
import logging
import ConfigParser
cf = ConfigParser.ConfigParser()
cf.read("conf/recommend.ini")
logpath=cf.get('log','logpath')+datetime.now().strftime('%Y-%m-%d')+'.log'
logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                filename=logpath,
                filemode='a')





