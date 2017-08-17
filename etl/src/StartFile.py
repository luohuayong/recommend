# -*- coding: utf-8 -*-
import psycopg2
from apscheduler.schedulers.blocking import BlockingScheduler
import logging
import loghelper
import DBsqlserver
import GetConfig
import GetproductState

def main():
    logging.info(u'---------game start-----------')
    sqlcon = DBsqlserver.MSSQL(host=GetConfig.sqlserverhost, user=GetConfig.sqlserveruser, pwd=GetConfig.sqlserverpwd, db=GetConfig.sqlserverdbname,port=GetConfig.sqlserverport)
    conn = psycopg2.connect(database=GetConfig.pgdbname, user=GetConfig.pguser,password=GetConfig.pgpwd,host=GetConfig.pghost, port=GetConfig.pgport)
    grescon=conn.cursor()
    # 订单购买表
    try:

        logging.info(u'开始导入订单购买表，这是已支付的')
        sql_buyed=""" select  bo.uid,bop.pid,(DATEDIFF(S,'1970-01-01 00:00:00', bo.paytime) - 8 * 3600) as ptime from bma_orders bo
                    left join bma_orderproducts bop on bo.oid=bop.oid and bo.orderstate in(70,110,140)
                    where bo.paytime!='1900-01-01 00:00:00.000' and bo.paytime is not null and pid is not null """
        res_buyed = sqlcon.ExecQuery(sql_buyed)
        logging.info(u'开始插入订单购买表')
        if res_buyed:
            delete_buyed_sql='delete from data_payment'
            delete_buyed_result=grescon.execute(delete_buyed_sql)
            res_buyed_count=len(res_buyed)
            for_buyed_count=res_buyed_count/3000+1
            for i in range(for_buyed_count):
                buyed_list=[];
                insert_buyed_sql='insert into data_payment (uid,pid,ptime) values '
                for t in res_buyed[i*3000:(i+1)*3000]:
                    insert_buyed_sql=insert_buyed_sql+'(%s,%s,to_timestamp(%s))'+','
                    buyed_list.append(t[0])
                    buyed_list.append(t[1])
                    buyed_list.append(t[2])
                insert_buyed_sql=insert_buyed_sql[:-1]+';'
                grescon.execute(insert_buyed_sql,buyed_list)
                logging.info(u'订单购买表commit')
                conn.commit()
    except Exception, e:
        logging.exception(u'插入已支付订单购买表出现异常'+e.message)
        conn.rollback()
        return
    logging.info(u'已支付订单购买表导入成功')

    logging.info(u'---------我是华丽分割线-----------')
    try:
        logging.info(u'开始导入订单表，这是未支付的')
        sql_buying="""select  bo.uid,bop.pid,(DATEDIFF(S,'1970-01-01 00:00:00', bo.addtime) - 8 * 3600) as ptime from bma_orders bo
                    left join bma_orderproducts bop on bo.oid=bop.oid and bo.orderstate in(30,200,210)
                    where bo.uid is not null and pid is not null """
        res_buying = sqlcon.ExecQuery(sql_buying)
        if res_buying:
            delete_buying_sql='delete from data_order'
            delete_buying_result=grescon.execute(delete_buying_sql)
            res_buying_count=len(res_buying)
            for_buying_count=res_buying_count/3000+1
            for i in range(for_buying_count):
                buying_list=[];
                insert_buying_sql='insert into data_order (uid,pid,otime) values '
                for t in res_buying[i*3000:(i+1)*3000]:
                    insert_buying_sql=insert_buying_sql+'(%s,%s,to_timestamp(%s))'+','
                    buying_list.append(t[0])
                    buying_list.append(t[1])
                    buying_list.append(t[2])
                insert_buying_sql=insert_buying_sql[:-1]+';'
                grescon.execute(insert_buying_sql,buying_list)
                logging.info(u'支付订单购买表commit')
                conn.commit()
    except Exception, e:
        logging.exception(u'插入未支付订单表出现异常'+e.message)
        conn.rollback()
        return
    logging.info(u'未支付的订单表导入成功')

    logging.info(u'---------我是华丽分割线-----------')
    try:
        logging.info(u'开始导入购物车表')
        sql_cart="""  select  uid,pid, (DATEDIFF(S,'1970-01-01 00:00:00', addtime) - 8 * 3600) as ctime from bma_carts """
        res_cart = sqlcon.ExecQuery(sql_cart)
        if res_cart:
            delete_cart_sql='delete from data_cart'
            delete_cart_result=grescon.execute(delete_cart_sql)
            logging.info(u'购物车表开始插入')
            res_cart_count=len(res_cart)
            for_cart_count=res_cart_count/3000+1
            for i in range(for_cart_count):
                cart_list=[];
                insert_cart_sql='insert into data_cart (uid,pid,ctime) values '
                for t in res_cart[i*3000:(i+1)*3000]:
                    insert_cart_sql=insert_cart_sql+'(%s,%s,to_timestamp(%s))'+','
                    cart_list.append(t[0])
                    cart_list.append(t[1])
                    cart_list.append(t[2])
                insert_cart_sql=insert_cart_sql[:-1]+';'
                grescon.execute(insert_cart_sql,cart_list)
                logging.info(u'购物车表commit')
                conn.commit()
    except Exception, e:
        logging.exception(u'插入购物车表出现异常'+e.message)
        conn.rollback()
        return
    logging.info(u'购物车表导入成功')
    logging.info(u'---------我是华丽分割线-----------')
    try:
        logging.info(u'开始导入收藏夹表')
        sql_favorites="""  select  uid,pid, (DATEDIFF(S,'1970-01-01 00:00:00', addtime) - 8 * 3600) as ftime from bma_favoriteproducts """
        res_favorites = sqlcon.ExecQuery(sql_favorites)
        if res_favorites:
            delete_favorites_sql='delete from data_favorites'
            delete_result=grescon.execute(delete_favorites_sql)
            res_favorites_count=len(res_favorites)
            forcount=res_favorites_count/3000+1
            for i in range(forcount):
                favorites_list=[];
                insert_favorites_sql='insert into data_favorites (uid,pid,ftime) values '
                for t in res_favorites[i*3000:(i+1)*3000]:
                    insert_favorites_sql=insert_favorites_sql+'(%s,%s,to_timestamp(%s))'+','
                    favorites_list.append(t[0])
                    favorites_list.append(t[1])
                    favorites_list.append(t[2])
                insert_favorites_sql=insert_favorites_sql[:-1]+';'
                grescon.execute(insert_favorites_sql,favorites_list)
                conn.commit()
    except Exception, e:

        logging.exception(u'插入收藏夹表表出现异常'+e.message)
        conn.rollback()
        return
    logging.info(u'收藏夹表导入成功')
    conn.close()

    logging.info(u'--------------game over-----------------')
    print (u'--------------game over-----------------')

if __name__ == '__main__':
    print(u'---------game start-----------')
    main()
    # isTimer=GetConfig.isTimer
    # if isTimer:
    #     minute=GetConfig.minute
    #     hour=GetConfig.hour
    #     day=GetConfig.day
    #     scheduler = BlockingScheduler()
    #     scheduler.add_job(main,'cron',minute=47,hour=10,day='*')
    #     scheduler.add_job(GetproductState.ProductCollect,'cron',minute=50,hour=10,day='*')
    #     try:
    #        scheduler.start()
    #     except (KeyboardInterrupt, SystemExit):
    #         scheduler.shutdown()
    # else:
    #     main()


