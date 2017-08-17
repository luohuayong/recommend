__author__ = 'Administrator'

from django.conf.urls import patterns, include, url
from api import views

urlpatterns = [
    # url(r'^getRecommendList/$', views.UserRecommendList.as_view()),
    url(r'^recommend/products$', views.ProductDetailRecommend.as_view()),
    url(r'^recommend/carts$', views.CartRecommend.as_view()),
    url(r'^recommend/browse', views.DataBrowse.as_view()),
    url(r'^recommend/search', views.DataSearch.as_view()),
]