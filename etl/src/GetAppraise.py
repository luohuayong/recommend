# -*- coding: utf-8 -*-
import  GetConfig
import psycopg2
import logging
import loghelper
import MySQLdb

""" 获取用户评价 """
def appraise():
    logging.info(u'---------appraiseCollect start-----------')
    #mysql info
    host=GetConfig.mysqlhost
    user=GetConfig.mysqluser
    passwd=GetConfig.mysqlpwd
    db=GetConfig.mysqldbname
    port=GetConfig.mysqlport
    #先查询pg库中最后一条记录的时间，然后到mysql中导出这个时间之后的记录 采用增量的方式
    try:
        MySQLconn=MySQLdb.connect(host=host,user=user,passwd=passwd,db=db,port=port)
        cur=MySQLconn.cursor()

        pgconn = psycopg2.connect(database=GetConfig.pgdbname, user=GetConfig.pguser,password=GetConfig.pgpwd,host=GetConfig.pghost, port=GetConfig.pgport)
        grescon=pgconn.cursor()

        sql_last_time="""
        select to_char(rtime,'yyyy-mm-dd HH24:MI:ss') from data_rating order by rtime desc limit 1
        """
        grescon.execute(sql_last_time)
        time_result=grescon.fetchone()
        count=0
        if time_result:
            logging.info(time_result[0])
            sql="""
            select aid ,pid,grade/10.0 as rating,UNIX_TIMESTAMP(createdAt) as createdAt from feedback where aid is not null and state=2 and createdAt> %s;
            """
            count=cur.execute(sql,[time_result[0]])
        else:
            sql="""
            select aid ,pid,grade/10.0 as rating,UNIX_TIMESTAMP(createdAt) as createdAt from feedback where aid is not null and state=2 ;
            """
            count=cur.execute(sql)
        logging.info(count)
        results=cur.fetchall()
        cur.close()
        MySQLconn.close()

        if  results:
            # delete_product_sql='delete from data_rating'
            # delete_product_result=grescon.execute(delete_product_sql)
            res_appraise_count=len(results)
            for_appraise_count=res_appraise_count/3000+1
            for i in xrange(for_appraise_count):
                appraise_list=[]
                insert_appraise_sql='insert into data_rating (uid,pid,rating,rtime) values '
                for t in results[i*3000:(i+1)*3000]:
                    insert_appraise_sql=insert_appraise_sql+'(%s,%s,%s,to_timestamp(%s))'+','
                    appraise_list.append(t[0])
                    appraise_list.append(t[1])
                    appraise_list.append(t[2])
                    appraise_list.append(t[3])
                insert_appraise_sql=insert_appraise_sql[:-1]+';'
                grescon.execute(insert_appraise_sql,appraise_list)
                logging.info(u'评价信息commit')
                pgconn.commit()
    except Exception, e:
        logging.exception(u'插入评价信息表出现异常'+e.message)
        pgconn.rollback()
        return
    logging.info(u'---------appraiseCollect success-----------')


if __name__ == '__main__':
    appraise()


