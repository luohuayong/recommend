import json
import numpy as np
from offline import init
sc = init.sc
log = init.log
rd = init.rd
pipe = init.pipe
conn = init.conn
cur = init.cur

def cosineSimilarity(x,y):
    return np.dot(x,y)/(np.linalg.norm(x)*np.linalg.norm(y))

def product_similarity_run(mod):
    log.info("product_similarity delete...")
    sql_del_product_similarity = "delete from product_similarity"
    cur.execute(sql_del_product_similarity)
    conn.commit()

    log.info("product_similarity insert start...")
    rdd_feature = mod.productFeatures()
    rdd_feature.cache()
    list_feature = rdd_feature.collect()
    sql_values = ""
    rows_num = 0
    list_product_similarity = []
    for i in range(len(list_feature)):
        pid,pFactor = list_feature[i]
        sims = rdd_feature.map(lambda (id,factor):(id,cosineSimilarity(factor,pFactor)))
        sims.cache()
        # slow,bug begin
        #import pudb; pu.db
        #log.info("%s" % sims.count())
        item_similarity = sims.sortBy((lambda x:x[1]),ascending = False)\
            .filter(lambda x:x[0] != pid).take(30)
        # slow,bug end
        list_product_similarity.append((pid,item_similarity))
        for j in range(len(item_similarity)):
            row = item_similarity[j]
            sql_values += "(%s,%s,%s)," % (pid,row[0],row[1])
            rows_num += 1
        if (i != 0 and i % 100 == 0) or i == len(list_feature) - 1:
            sql_insert = "insert into product_similarity (pid,spid,similarity) values %s"\
                % sql_values.rstrip(',')
            sql_values = ""
            cur.execute(sql_insert)
            conn.commit()
    log.info("product_similarity(%s products and %s rows) insert complete!" % \
            (len(list_feature),rows_num))

    log.info("product_similarity write redis...")
    redis_prefix = "rec.product_similarity.pid"
    for i in range(len(list_product_similarity)):
        row = list_product_similarity[i]
        json_value = json.dumps(row[1])
#        log.info("%s" % i)
        rd.set("%s:%s" % (redis_prefix,row[0]),json_value)
   # pipe.execute()
    log.info("product_similarity write redis complete!")


#from offline import user_rating
#from offline import train_model
#from offline import user_recommend
#from offline import product_similarity
#from offline import product_hot
#from offline import user_cart_recommend
#import offline.*
from offline import *
user_rating.run()
mod = train_model.run()
#product_similarity.run(mod)
product_similarity_run(mod)
user_recommend.run(mod)
product_hot.run()
user_cart_recommend.run()

