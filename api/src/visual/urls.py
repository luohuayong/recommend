__author__ = 'Administrator'

from django.conf.urls import patterns, include, url
from visual import views

urlpatterns = [
    url(r'^recommend/user2products/$', views.user2products),
    url(r'^recommend/product2products/$', views.product2products),
    url(r'^recommend/cart2products/$', views.cart2products),
    url(r'^recommend/charts/$', views.charts),
]