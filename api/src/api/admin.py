# -*- coding: utf-8 -*-

from django.contrib import admin
from api.models import DataFavorites,UserRecommend

# Register your models here.
class DataFavoritesAdmin(admin.ModelAdmin):
    list_display = ('uid', 'pid', 'ftime')
    search_fields = ('uid', 'pid')

class UserRecommendAdmin(admin.ModelAdmin):
    list_display = ('uid', 'pid', 'rating')
    search_fields = ('uid', 'pid')


admin.site.register(DataFavorites, DataFavoritesAdmin)
admin.site.register(UserRecommend, UserRecommendAdmin)




