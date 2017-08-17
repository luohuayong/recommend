# -*- coding:utf-8 -*-
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from api.models import UserRecommend, ProductSimilarity, UserCartRecommend, ProductHot, DataProduct
from api.serializers import UserRecommendSerializer, ProductSimilaritySerializer, DataBrowseSerializer, DataSearchSerializer, ProductHotSerializer, UserCartRecommendSerializer
from config import cf, logger, rd
from itertools import chain
import json
import kafka
import requests
import redis

class UserRecommendList(APIView):
    def get(self, request, format=None):
        snippets = UserRecommend.objects.all()
        serializer = UserRecommendSerializer(snippets, many=True)
        return Response(serializer.data)

# 商品详情推荐
class ProductDetailRecommend(APIView):
    def get_products(self, uid, pid, count):
        try:
            products = ProductSimilarity.objects.raw('SELECT ps.* FROM product_similarity ps '
                                                 ' left join data_product dp on ps.spid=dp.pid '
                                                 ' where dp.status=1 and ps.pid=%s and ps.spid != %s order by similarity desc limit %s' % (pid, pid, count))
            serializer = ProductSimilaritySerializer(products, many=True)

            # 由于序列化的key值不同，所以进行list复制
            alist = []
            if serializer.data:
                for item in serializer.data:
                    d = dict()
                    d['pid'] = item['spid']
                    d['rating'] = item['similarity']
                    alist.append(d)
            else:
                # 若无则读取redis，返回热销商品
                products = ProductHot.objects.raw('SELECT ph.* FROM product_hot ph '
                                                 ' left join data_product dp on ph.pid=dp.pid '
                                                 ' where dp.status=1 and ph.pid != %s order by hot desc limit %s' % (pid, count))
                serializer = ProductHotSerializer(products, many=True)
                if serializer.data:
                    for item in serializer.data:
                        d = dict()
                        d['pid'] = item['pid']
                        d['rating'] = item['hot']
                        alist.append(d)
            return alist
        except ProductDetailRecommend.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        pjson = {}
        try:
            logger.info('/recommend/products')
            logger.info(request.GET)
            # uid = request.GET.get('uid') if request.GET.get('uid') not in (None, '') else 0
            # pid = request.GET.get('pid') if request.GET.get('pid') not in (None, '') else 0
            uid = request.GET.get('uid', 0)
            pid = request.GET.get('pid', 0)
            recproducts = self.get_products(uid, pid, cf.get("api", "reccount"))
            # raise ValueError('input error!')
            if recproducts:
                pjson['ret'] = 0
                pjson['msg'] = 'success'
                pjson['data'] = recproducts
            else:
                pjson['ret'] = 1
                pjson['msg'] = u'无此商品推荐数据'
        except Exception, e:
            pjson['ret'] = 1
            pjson['msg'] = str(e)
        finally:
            logger.info(pjson)
            return Response(pjson)

# 购物车推荐(读redis)
class CartRecommend(APIView):
    def get_products(self, uid, count):
        try:
            # 查询购物车有无推荐
            cartproducts = rd.get('rec.user_cart_recommend.uid:' + str(uid))
            userproducts = rd.get('rec.user_recommend.uid:' + str(uid))
            pidlist = []
            if cartproducts:
                if userproducts:
                    for item in json.loads(cartproducts):
                        pidlist.append(str(item[1]))
                    for item in json.loads(userproducts):
                        pidlist.append(str(item[1]))
                else:
                    for item in json.loads(cartproducts):
                        pidlist.append(str(item[1]))
            else:
                if userproducts:
                    for item in json.loads(userproducts):
                        pidlist.append(str(item[1]))
                else:
                    products = rd.get('rec.product_hot')
                    for item in json.loads(products)[:30]:
                        pidlist.append(str(item[0]))

            # 筛选出所有上架的商品
            p = DataProduct.objects.filter(pid__in=pidlist).filter(status=1)

            pidslist = []
            for item in p[:6]:
                pidslist.append(item.pid)

            # 若数量小于6个则取在售商品补全(低概率)
            if len(pidslist) < 6:
                length = 6 - len(pidslist)
                p1 = DataProduct.objects.exclude(pid__in=pidlist).filter(status=1)[:length]
                for item in p1:
                    pidslist.append(item.pid)

            # 去重
            # new_pids = list(set(pidlist))[:12]

            pids = ','.join(map(str, pidslist))

            # 拼接商品详情图片、标题等信息
            url = cf.get("api", "baseurl") + '/products/1.1.0/products/list?type=1'
            postjson = {"pids": pids}
            headers = {'Client_Version': '1.7.1', 'Client_Type': '2'}
            r = requests.post(url, data=postjson, headers=headers)
            rjson = json.loads(r.text)
            alist = []
            if rjson['ret'] == 0:
                for item in rjson['data']:
                    d = dict()
                    d['_id'] = item['_id']
                    d['img'] = item['img']
                    d['market_price'] = item['price']
                    d['price'] = item['shopprice']
                    d['title'] = item['title']
                    alist.append(d)
            return alist
        except Exception, e:
            raise e

    def get(self, request, format=None):
        pjson = {}
        try:
            logger.info('/recommend/carts')
            uid = request.GET.get('uid', 0)

            recproducts = self.get_products(uid, cf.get("api", "reccount"))
            if recproducts:
                pjson['ret'] = 0
                pjson['msg'] = 'success'
                pjson['data'] = recproducts
            else:
                pjson['ret'] = 1
                pjson['msg'] = u'无此用户购物车推荐数据'
        except Exception, e:
            pjson['ret'] = 1
            pjson['msg'] = str(e)
        finally:
            logger.info(pjson)
            return Response(pjson)

class DataBrowse(APIView):
    def post(self, request, format=None):
        logger.info('/recommend/browse')
        logger.info(request.data)
        rjson = {}
        try:
            # 将信息传入kafka队列
            request.data['method'] = 'browse'
            kafka.produce(json.dumps(request.data))
            rjson['ret'] = 0
            rjson['msg'] = 'success'

            # serializer = DataBrowseSerializer(data=request.data)
            # if serializer.is_valid():
            #     serializer.save()
            #     rjson['ret'] = 0
            #     rjson['msg'] = 'success'
            # else:
            #     raise ValueError(serializer.errors)
        except Exception, e:
            rjson['ret'] = 1
            rjson['msg'] = str(e)
        finally:
            logger.info(rjson)
            return Response(rjson)

class DataSearch(APIView):
    def post(self, request, format=None):
        logger.info('/recommend/search')
        logger.info(request.data)
        rjson = {}
        try:
            # 将信息传入kafka队列
            request.data['method'] = 'search'
            kafka.produce(json.dumps(request.data))
            rjson['ret'] = 0
            rjson['msg'] = 'success'

            # rjson['ret'] = 0
            # rjson['msg'] = 'success'
            # serializer = DataSearchSerializer(data=request.data)
            # if serializer.is_valid():
            #     serializer.save()
            #     rjson['ret'] = 0
            #     rjson['msg'] = 'success'
            # else:
            #     raise ValueError(serializer.errors)
        except Exception, e:
            rjson['ret'] = 1
            rjson['msg'] = str(e)
        finally:
            logger.info(rjson)
            return Response(rjson)





