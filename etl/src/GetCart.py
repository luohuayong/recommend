# -*- coding: utf-8 -*-


import GetConfig
import DBsqlserver
from pykafka import  KafkaClient
import logging
import loghelper
import ConfigParser
cfr = ConfigParser.ConfigParser()
cfr.read("conf/realtime.ini")

# import datetime
# import  time

# import json
# from elasticsearch import Elasticsearch


def GetCart():
    try:
        logging.info(u"----------获取购物车信息 start-----------")
        cart=cfr.getfloat("weights", "cart")

        env=cfr.get("environment", "env")

        topicscart=''
        if env=='dev':
            topicscart='dev.rec.user_cart'
        elif   env=='sit':
            topicscart='sit.rec.user_cart'
        elif    env=='pre':
            topicscart='pre.rec.user_cart'
        elif env=='prd':
            topicscart='rec.user_cart'
        client=KafkaClient(hosts=GetConfig.hosts)
        topic=client.topics[topicscart]
        sqlcon = DBsqlserver.MSSQL(host=GetConfig.sqlserverhost, user=GetConfig.sqlserveruser, pwd=GetConfig.sqlserverpwd, db=GetConfig.sqlserverdbname,port=GetConfig.sqlserverport)
        # 购物车
        cartid=cfr.getint("latestdata", "cartid")
        sql_cart="""    select max(bc.cartid) as cartid , bc.uid , [val]=(
      select cast([pid] as varchar(50))+','  from bma_carts cart where  bc.uid=cart.uid for xml path('')
      )

      from bma_carts bc where bc.cartid >%s group by uid order by cartid"""
        res_cart = sqlcon.ExecQuery(sql_cart,cartid)
        if res_cart:
            with topic.get_sync_producer() as producer:
                for t in res_cart:
                    cartid=t[0]
                    message=str(t[1])+','+str(t[2])[:-1]
                    print message
                    producer.produce(message)
            cfr.set("latestdata", "cartid",cartid)
            cfr.write(open("conf/realtime.ini", "w"))
        logging.info(u"----------获取购物车信息 end-----------")
    except Exception, e:
        logging.exception(u'获取购物车信息出现异常'+e.message)
        logging.exception(u"----------获取购物车信息 fail-----------")
        return

if __name__ == '__main__':
    GetCart()