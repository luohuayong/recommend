__author__ = 'Administrator'
from django.forms import widgets
from rest_framework import serializers
from api.models import UserRecommend, ProductSimilarity, DataBrowse, DataSearch, ProductHot, UserCartRecommend

class UserRecommendSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRecommend
        fields = ('pid', 'rating')

class ProductSimilaritySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSimilarity
        fields = ('spid', 'similarity')

class DataBrowseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataBrowse

class DataSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSearch

class ProductHotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductHot

class UserCartRecommendSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCartRecommend