import recommend
import json
import init
sc = init.sc
log = init.log
rd = init.rd
pipe = init.pipe
conn = init.conn
cur = init.cur
consumer = init.consumer

log.info("make rdd_product_similarity...")
sql_similarity = "select pid,spid,similarity from product_similarity"
cur.execute(sql_similarity)
rdd_product_similarity = sc.parallelize(cur.fetchall())

def run():

    #log.info("subscribe kafka[%s] topic[%s] group[%s]:" % \
    #    (ka_hosts,ka_topics,ka_group))
    while True:
        message = consumer.consume()
        consumer.commit_offsets()
        try:
            log.info(message.value)
            row = message.value.split(',')
            uid = row[0]
            pids = row[1::]
            rating = map(lambda x:(int(uid),int(x),7.0),pids)
            rdd1 = sc.parallelize(rating)


        #    rdd1 = sc.parallelize([(int(row[0]),int(row[1]),float(row[2]))])
            rdd2 = recommend.recommend(rdd_product_similarity,rdd1)
            list_rdd2 = rdd2.take(30)#.collect()
            log.info(list_rdd2)

        #    log.info("redis write start ...")
            redis_prefix = "rec.user_cart_recommend.uid"
            json_value = json.dumps(list_rdd2)
            rd.set("%s:%s" % (redis_prefix,list_rdd2[0][0]),json_value)
        except Exception,e:
            log.error(e)


