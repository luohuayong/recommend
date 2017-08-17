# -*- coding: utf-8 -*-
"""
实时计算
"""
import GetConfig
import DBsqlserver
from pykafka import  KafkaClient
import logging
import loghelper
import ConfigParser
cfr = ConfigParser.ConfigParser()
cfr.read("conf/realtime.ini")

import datetime
import  time

import json
from elasticsearch import Elasticsearch


def realtime():



    cart=cfr.getfloat("weights", "cart")
    order=cfr.getfloat("weights", "order")
    payment=cfr.getfloat("weights", "payment")
    favorite=cfr.getfloat("weights", "favorite")
    browse=cfr.getfloat("weights", "browse")



    client=KafkaClient(hosts=GetConfig.hosts)
    topic=client.topics[GetConfig.topics]
    sqlcon = DBsqlserver.MSSQL(host=GetConfig.sqlserverhost, user=GetConfig.sqlserveruser, pwd=GetConfig.sqlserverpwd, db=GetConfig.sqlserverdbname,port=GetConfig.sqlserverport)

    # 购物车
    # cartid=cfr.getint("latestdata", "cartid")
    # sql_cart="""  select  cartid, uid,pid from bma_carts where cartid> %s  order by cartid """
    # res_cart = sqlcon.ExecQuery(sql_cart,cartid)
    # if res_cart:
    #     with topic.get_sync_producer() as producer:
    #         for t in res_cart:
    #             cartid=t[0]
    #             message=str(t[1])+','+str(t[2])+','+cart
    #             producer.produce(message)
    #     cfr.set("latestdata", "cartid",cartid)
    #     cfr.write(open("conf/realtime.ini", "w"))

    #   收藏夹
    # favid=cfr.getint("latestdata", "favid")
    # sql_fav="""  select  recordid, uid,pid from bma_carts where recordid> %s  order by cartid """
    # res_cart = sqlcon.ExecQuery(sql_fav,favid)
    # if res_cart:
    #     with topic.get_sync_producer() as producer:
    #         for t in res_cart:
    #             favid=t[0]
    #             message=str(t[1])+','+str(t[2])+','+favorite
    #             producer.produce(message)
    #     cfr.set("latestdata", "favid",favid)
    #     cfr.write(open("conf/realtime.ini", "w"))



    eshost=cfr.get("Elasticsearch", "host")
    port=cfr.getint("Elasticsearch", "port")
    es = Elasticsearch([{'host':eshost,'port':port}])




    time_now=time.strftime('%Y.%m.%d',time.localtime(time.time()))
    indexname='logstash-hp-win-prd-'+time_now

    DayAgo = (datetime.datetime.now() - datetime.timedelta(days = 1))
    DayAgoTime = DayAgo.strftime("%Y.%m.%d")
    indexnameAgo='logstash-hp-win-prd-'+DayAgoTime
    index=[indexnameAgo,indexname]

    logging.info(u'----------------------------------es采集 start----------------------------------')
    # logging.info(u'索引名称::%s',index)
    #用户浏览信息 通过es获取
    # logging.info(u"----------用户浏览信息 start-----------")
    # browsetime=cfr.get("latestdata", "browsetime")
    # logging.info(u"开始时间戳:%s",browsetime)
    # browsebody={"fields":['msg.http_header.Auth_Account','msg.input','@timestamp'],
    #     'query':
    #     {'filtered':
    #         {'filter':
    #             {'range':
    #                 {'@timestamp':{'gt':browsetime}},
    #             },
    #          "query":{
    #          "bool": {
    #             "must": [
    #                 { "match":  {"action":"1" }},
    #                 { "match": {"context_name":"Hopin.Service.Product.Apis.Web_GetProductDetailApi" }},
    #                  ],
    #                "must_not":[
    #                      { "match":  {"msg.http_header.Auth_Account":"0" }},
    #              ]
    #             }
    #         }
    #     }
    #     },
    #       "sort": { "@timestamp": { "order": "esc" } }
    # }
    # # 获用户浏览信息
    # encodedjson = es.search(index=index,body=browsebody,size=10000)
    # hits=encodedjson['hits']['hits']
    # if hits:
    #     logging.info(hits)
    #     with topic.get_sync_producer() as producer:
    #         for item in hits:
    #             browsetime=item['fields']['@timestamp'][0]
    #             message=str(item['fields']['msg.http_header.Auth_Account'][0])+','+str(item['fields']['msg.input'][0].strip('\"'))+','+str(browse)
    #             producer.produce(message)
    #     cfr.set("latestdata", "browsetime",browsetime)
    #     logging.info(u"结束时间戳:%s",browsetime)
    #     cfr.write(open("conf/realtime.ini", "w"))
    #     logging.info(u"----------用户浏览信息 end-----------")
    #
    #
    #
    # #获取用户收藏信息
    # logging.info(u"----------获取用户收藏信息 start-----------")
    # favoritetime=cfr.get("latestdata", "favoritetime")
    # logging.info(u"开始时间戳:%s",favoritetime)
    # favoritebody={"fields":['msg.http_header.Auth_Account','msg.input','@timestamp'],
    #     'query':
    #     {'filtered':
    #         {'filter':
    #             {'range':
    #                 {'@timestamp':{'gt':favoritetime}},
    #             },
    #          "query":{
    #          "bool": {
    #             "must": [
    #                 { "match":  {"action":"1" }},
    #                 { "match": {"context_name":"Hopin.Service.Product.Apis.Web_AddCollectApi" }},
    #                  ],
    #              "must_not":[
    #                      { "match":  {"msg.http_header.Auth_Account":"0" }},
    #              ]
    #             }
    #         }
    #     }
    #     },
    #       "sort": { "@timestamp": { "order": "esc" } }
    # }
    # favoritejson = es.search(index=index,body=favoritebody,size=10000)
    # favoritehits=favoritejson['hits']['hits']
    # if favoritehits:
    #     logging.info(favoritehits)
    #     with topic.get_sync_producer() as producer:
    #         for item in favoritehits:
    #             favoritetime=item['fields']['@timestamp'][0]
    #             message=str(item['fields']['msg.http_header.Auth_Account'][0])+','+str(item['fields']['msg.input'][0].strip('\"'))+','+str(favorite)
    #             producer.produce(message)
    #     cfr.set("latestdata", "favoritetime",favoritetime)
    #     logging.info(u"结束时间戳:%s",favoritetime)
    #     cfr.write(open("conf/realtime.ini", "w"))
    #     logging.info(u"----------获取用户收藏信息 end-----------")
    #
    # #获取购物车信息
    # logging.info(u"----------获取购物车信息 start-----------")
    # carttime=cfr.get("latestdata", "carttime")
    # logging.info(u"开始时间戳:%s",carttime)
    # cartbody={"fields":['msg.http_header.Auth_Account','msg.input','@timestamp'],
    #     'query':
    #     {'filtered':
    #         {'filter':
    #             {'range':
    #                 {'@timestamp':{'gt':carttime}},
    #             },
    #          "query":{
    #          "bool": {
    #             "must": [
    #                 { "match":  {"action":"1" }},
    #                 { "match": {"context_name":"Hopin.Service.Order.Apis.Cart.PostAddCartApi" }},
    #                  ]
    #             }
    #         }
    #     }
    #     },
    #       "sort": { "@timestamp": { "order": "esc" } }
    # }
    # cartjson = es.search(index=index,body=cartbody,size=10000)
    # carthits=cartjson['hits']['hits']
    # if carthits:
    #     logging.info(carthits)
    #     with topic.get_sync_producer() as producer:
    #         for item in carthits:
    #             carttime=item['fields']['@timestamp'][0]
    #             message=str(item['fields']['msg.http_header.Auth_Account'][0])+','+str(json.loads(item['fields']['msg.input'][0])['pid'])+','+str(cart)
    #             producer.produce(message)
    #     cfr.set("latestdata", "carttime",carttime)
    #     logging.info(u"结束时间戳:%s",carttime)
    #     cfr.write(open("conf/realtime.ini", "w"))
    #     logging.info(u"----------获取购物车信息 end-----------")


    #获取订单信息
    logging.info(u"----------获取订单信息 start-----------")
    ordertime=cfr.get("latestdata", "ordertime")
    logging.info(u"开始时间戳:%s",ordertime)
    orderbody={"fields":['msg.http_header.Auth_Account','msg.input','@timestamp'],
        'query':
        {'filtered':
            {'filter':
                {'range':
                    {'@timestamp':{'gt':ordertime}},
                },
             "query":{
             "bool": {
                "must": [
                    { "match":  {"action":"1" }},
                    { "match": {"context_name":"Hopin.Service.Order.Apis.Order.PostAddOrderApi" }},
                     ]
                }
            }
        }
        },
          "sort": { "@timestamp": { "order": "esc" } }
    }
    orderjson = es.search(index=index,body=orderbody,size=10000)
    orderhits=orderjson['hits']['hits']
    if orderhits:
        logging.info(orderhits)
        with topic.get_sync_producer() as producer:
            for item in orderhits:
                ordertime=item['fields']['@timestamp'][0]
                for pid in json.loads(item['fields']['msg.input'][0])['pidlist']:
                    message=str(item['fields']['msg.http_header.Auth_Account'][0])+','+str(pid['pid'])+','+str(order)
                    producer.produce(message)
        cfr.set("latestdata", "ordertime",ordertime)
        logging.info(u"结束时间戳:%s",ordertime)
        cfr.write(open("conf/realtime.ini", "w"))
        logging.info(u"----------获取订单信息 end-----------")
    logging.info(u'----------------------------------es采集 end----------------------------------')
if __name__ == '__main__':
    realtime()



