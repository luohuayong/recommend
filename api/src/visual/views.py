# -*- coding:utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response,render
from django.core.context_processors import csrf
import requests
import json
from config import cf, rd
from collections import Counter
from api.models import UserRecommend,DataPayment,DataFavorites,DataCart,DataOrder,ProductSimilarity,DataBrowse, DataSearch


# 用户推荐商品页面
def user2products(request):
    ctx = {}
    ctx.update(csrf(request))

    uid = 0

    if request.POST:
        uid = request.POST['q'] if request.POST['q'] != '' else 0

    # 随机取三个商品
    response = UserRecommend.objects.filter(uid=uid)
    pids = ''
    for i in response:
        pids += str(i.pid) + ','

    # 调用接口获取推荐信息
    # url1 = 'http://192.168.1.193:8088/rest/getRecommendByuid/'+str(uid)
    # r1 = requests.get(url1)
    # rjson1 = json.loads(r1.text)
    # pids = ''
    # if rjson1['ret'] == 0:
    #     for item in rjson1['data']:
    #         pids += str(item['pid']) + ','

    # 获取商城商品信息
    url = cf.get("api", "baseurl") + '/products/1.1.0/products/list?type=1'

    print url
    postjson = {"pids": pids[0:len(pids)-1]}
    headers = {'Client_Version': '1.7.1', 'Client_Type': '2'}
    r = requests.post(url, data=postjson, headers=headers)

    rjson = json.loads(r.text)
    # 拼接评分数据
    if rjson['ret'] == 0:
        for item in rjson['data']:
            item['pid'] = item['_id']
            item['rating'] = UserRecommend.objects.filter(uid=uid).get(pid=item['_id']).rating
            item['img'] = cf.get("api", "picserver") + item['img'].split('.')[0] + '$a1000X1000.' + item['img'].split('.')[1]

    # 拼接用户购买信息
    response1 = DataPayment.objects.filter(uid=uid)
    uinfo = ''
    for item in response1:
        uinfo += str(item.pid) + ','
    rjson['uinfo'] = u'用户' + str(uid) + u'购买过的商品有:' + uinfo[0:len(uinfo)-1]

    # 拼接用户订单信息
    response1 = DataOrder.objects.filter(uid=uid)
    uorder = ''
    for item in response1:
        uorder += str(item.pid) + ','
    rjson['uorder'] = u'用户' + str(uid) + u'未支付订单内的商品有:' + uorder[0:len(uorder)-1]

    # 拼接用户收藏信息
    response1 = DataFavorites.objects.filter(uid=uid)
    ufavorites = ''
    for item in response1:
        ufavorites += str(item.pid) + ','
    rjson['ufavorites'] = u'用户' + str(uid) + u'收藏过的商品有:' + ufavorites[0:len(ufavorites)-1]

    # 拼接用户购物车信息
    response1 = DataCart.objects.filter(uid=uid)
    ucart = ''
    for item in response1:
        ucart += str(item.pid) + ','
    rjson['ucart'] = u'用户' + str(uid) + u'购物车内的商品有:' + ucart[0:len(ucart)-1]

    ctx['rlt'] = rjson

    return render(request, "user2products.html", ctx)

# 商品关联商品页面
def product2products(request):
    ctx = {}
    ctx.update(csrf(request))
    pid = 0

    if request.POST:
        pid = request.POST['q'] if request.POST['q'] != '' else 0

    response = ProductSimilarity.objects.filter(pid=pid)

    # 第一行显示自身
    pids = str(pid) + ','
    for i in response:
        pids += str(i.spid) + ','
    print len(pids)
    if len(pids) > 2:
        # 获取商城商品信息
        url = cf.get("api", "baseurl") + '/products/1.1.0/products/list?type=1'
        postjson = {"pids": pids[0:len(pids)-1]}
        headers = {'Client_Version': '1.7.1', 'Client_Type': '2'}
        r = requests.post(url, data=postjson, headers=headers)

        rjson = json.loads(r.text)

        # 拼接关联数据
        if rjson['ret'] == 0:
            p = rjson['data'].pop(0)
            p['img'] = cf.get("api", "picserver") + p['img'].split('.')[0] + '$a1000X1000.' + p['img'].split('.')[1]
            p['pid'] = p['_id']
            for item in rjson['data']:
                item['pid'] = item['_id']
                item['similarity'] = ProductSimilarity.objects.filter(pid=pid).get(spid=item['_id']).similarity
                item['img'] = cf.get("api", "picserver") + item['img'].split('.')[0] + '$a1000X1000.' + item['img'].split('.')[1]
        rjson['p'] = p
        ctx['rlt'] = rjson

    return render(request, "product2products.html", ctx)

# 购物车推荐商品页面
def cart2products(request):
    ctx = {}
    ctx.update(csrf(request))
    uid = 0

    if request.POST:
        uid = request.POST['q'] if request.POST['q'] != '' else 0

    # # 调用接口获取推荐信息
    # url = cf.get("api", "recurl") + 'api/recommend/carts?uid='+str(uid)
    # r = requests.get(url)
    # rjson = json.loads(r.text)
    # if rjson['ret'] == 0:
    #     for item in rjson['data']:
    #         item['pid'] = item['_id']
    #         item['img'] = cf.get("api", "picserver") + item['img'].split('.')[0] + '$a1000X1000.' + item['img'].split('.')[1]

    products = rd.get('rec.user_cart_recommend.uid:' + str(uid))
    pids = ''
    if not products:
        # 查看用户有无推荐
        products = rd.get('rec.user_recommend.uid:' + str(uid))
        if not products:
            # 推荐热销商品
            products = rd.get('rec.product_hot')
            for item in json.loads(products)[:6]:
                pids += str(item[0]) + ','
        else:
            for item in json.loads(products)[:6]:
                pids += str(item[1]) + ','
    else:
        for item in json.loads(products)[:6]:
            pids += str(item[1]) + ','

    # 拼接商品详情图片、标题等信息
    url = cf.get("api", "baseurl") + '/products/1.1.0/products/list?type=1'
    postjson = {"pids": pids[0:len(pids)-1]}
    headers = {'Client_Version': '1.7.1', 'Client_Type': '2'}
    r = requests.post(url, data=postjson, headers=headers)
    rjson = json.loads(r.text)
    if rjson['ret'] == 0:
        for item in rjson['data']:
            item['pid'] = item['_id']
            item['market_price'] = item['price']
            item['price'] = item['shopprice']
            item['title'] = item['title']
            item['img'] = cf.get("api", "picserver") + item['img'].split('.')[0] + '$a1000X1000.' + item['img'].split('.')[1]
    ctx['rlt'] = rjson

    return render(request, "cart2products.html", ctx)

def charts(request):
    # 浏览记录
    browse = DataBrowse.objects.all()
    b = [bro.from_page for bro in browse]
    bcounts = Counter(b)

    # print counts.most_common(10)
    browser_stats = bcounts.most_common(20)

    # 搜索记录
    search = DataSearch.objects.all()
    s = [sea.content for sea in search]
    scount = Counter(s)

    search_stats = scount.most_common(50)
    return render(request, 'charts.html', locals())