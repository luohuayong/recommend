# -*- coding: utf-8 -*-
import psycopg2
import logging
import loghelper
import DBsqlserver
import  GetConfig
from apscheduler.schedulers.blocking import BlockingScheduler

sqlserverhost=GetConfig.sqlserverhost
sqlserveruser=GetConfig.sqlserveruser
sqlserverpwd=GetConfig.sqlserverpwd
sqlserverdbname=GetConfig.sqlserverdbname
sqlserverport=GetConfig.sqlserverport

pghost=GetConfig.pghost
pguser=GetConfig.pguser
pgpwd=GetConfig.pgpwd
pgdbname=GetConfig.pgdbname
pgport=GetConfig.pgport

""" 获取商品状态 """
def ProductCollect():
    logging.info(u'---------ProductCollect start-----------')
    try:
        sqlcon = DBsqlserver.MSSQL(host=sqlserverhost, user=sqlserveruser, pwd=sqlserverpwd, db=sqlserverdbname,port=sqlserverport)
        conn = psycopg2.connect(database=pgdbname, user=pguser,password=pgpwd,host=pghost, port=pgport)
        grescon=conn.cursor()
        sql_product="""select bp.pid,bp.state,bp.displays from bma_products bp  """
        res_product = sqlcon.ExecQuery(sql_product)
        if res_product:
            delete_product_sql='delete from data_product'
            delete_product_result=grescon.execute(delete_product_sql)
            res_product_count=len(res_product)
            for_product_count=res_product_count/3000+1
            for i in range(for_product_count):
                product_list=[]
                insert_product_sql='insert into data_product (pid,status) values '
                for t in res_product[i*3000:(i+1)*3000]:
                    insert_product_sql=insert_product_sql+'(%s,%s)'+','
                    product_list.append(t[0])
                    if t[1]==1 and t[2]==1:
                        product_list.append(1)
                    else:
                        product_list.append(0)
                insert_product_sql=insert_product_sql[:-1]+';'
                grescon.execute(insert_product_sql,product_list)
                logging.info(u'商品信息commit')
                conn.commit()
    except Exception, e:
        logging.exception(u'插入商品信息出现异常'+e.message)
        conn.rollback()
        return
    logging.info(u'---------ProductCollect success-----------')

if __name__ == '__main__':
    ProductCollect()
#     scheduler = BlockingScheduler()
#     # scheduler.add_job(main,'cron',minute=minute,hour=hour,day='*')
#     scheduler.add_job(ProductCollect,'cron',minute=35,hour=10,day='*')
#     try:
#        scheduler.start()
#     except (KeyboardInterrupt, SystemExit):
#         scheduler.shutdown()
#     # ProductCollect()