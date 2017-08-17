from __future__ import unicode_literals

from django.db import models

# Create your models here.
class DataBrowse(models.Model):
    uid = models.IntegerField()
    pid = models.IntegerField()
    btime = models.DateTimeField(blank=True, null=True)
    from_page = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'data_browse'


class DataCart(models.Model):
    uid = models.IntegerField()
    pid = models.IntegerField()
    ctime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data_cart'


class DataFavorites(models.Model):
    uid = models.IntegerField()
    pid = models.IntegerField()
    ftime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data_favorites'


class DataOrder(models.Model):
    uid = models.IntegerField()
    pid = models.IntegerField()
    otime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data_order'


class DataPayment(models.Model):
    uid = models.IntegerField()
    pid = models.IntegerField()
    ptime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data_payment'


class DataRating(models.Model):
    uid = models.IntegerField()
    pid = models.IntegerField()
    rating = models.FloatField(blank=True, null=True)
    rtime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data_rating'


class DataSearch(models.Model):
    uid = models.IntegerField()
    content = models.CharField(max_length=50)
    stime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data_search'

class ProductHot(models.Model):
    pid = models.IntegerField()
    hot = models.FloatField()

    class Meta:
        managed = False
        db_table = 'product_hot'

class ProductRecommend(models.Model):
    pid = models.IntegerField()
    rpid = models.IntegerField()
    rating = models.FloatField()

    class Meta:
        managed = False
        db_table = 'product_recommend'

class ProductSimilarity(models.Model):
    pid = models.IntegerField()
    spid = models.IntegerField()
    similarity = models.FloatField()

    class Meta:
        managed = False
        db_table = 'product_similarity'

class UserRating(models.Model):
    uid = models.IntegerField()
    pid = models.IntegerField()
    rating = models.FloatField()

    class Meta:
        managed = False
        db_table = 'user_rating'

class UserCartRecommend(models.Model):
    uid = models.IntegerField()
    pid = models.IntegerField()
    rating = models.FloatField()

    class Meta:
        managed = False
        db_table = 'user_cart_recommend'


class DataProduct(models.Model):
    pid = models.IntegerField()
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'data_product'

class UserRecommend(models.Model):
    uid = models.IntegerField()
    pid = models.IntegerField()
    rating = models.FloatField()
    # status = models.ForeignKey(DataProduct)

    class Meta:
        managed = False
        db_table = 'user_recommend'

class UserRecommendBak(models.Model):
    uid = models.IntegerField()
    pid = models.IntegerField()
    rating = models.FloatField()

    class Meta:
        managed = False
        db_table = 'user_recommend_bak'


class UserSimilarity(models.Model):
    uid = models.IntegerField()
    suid = models.IntegerField()
    similarity = models.FloatField()

    class Meta:
        managed = False
        db_table = 'user_similarity'