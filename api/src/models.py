# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class RecommendTest(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'Recommand_test'


class AppAccessrecord(models.Model):
    date = models.DateField()
    user_count = models.IntegerField()
    view_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'app_accessrecord'


class AppHost(models.Model):
    name = models.CharField(max_length=64)
    nagios_name = models.CharField(max_length=64, blank=True, null=True)
    ip = models.GenericIPAddressField(blank=True, null=True)
    internal_ip = models.GenericIPAddressField(blank=True, null=True)
    user = models.CharField(max_length=64)
    password = models.CharField(max_length=128)
    ssh_port = models.IntegerField(blank=True, null=True)
    status = models.SmallIntegerField()
    brand = models.CharField(max_length=64)
    model = models.CharField(max_length=64)
    cpu = models.CharField(max_length=64)
    core_num = models.SmallIntegerField()
    hard_disk = models.IntegerField()
    memory = models.IntegerField()
    system = models.CharField(max_length=32)
    system_version = models.CharField(max_length=32)
    system_arch = models.CharField(max_length=32)
    create_time = models.DateField()
    guarantee_date = models.DateField()
    service_type = models.CharField(max_length=32)
    description = models.TextField()
    idc = models.ForeignKey('AppIdc', models.DO_NOTHING)
    administrator = models.ForeignKey('AuthUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'app_host'


class AppHostgroup(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'app_hostgroup'


class AppHostgroupHosts(models.Model):
    hostgroup = models.ForeignKey(AppHostgroup, models.DO_NOTHING)
    host = models.ForeignKey(AppHost, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'app_hostgroup_hosts'
        unique_together = (('hostgroup', 'host'),)


class AppIdc(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    contact = models.CharField(max_length=32)
    telphone = models.CharField(max_length=32)
    address = models.CharField(max_length=128)
    customer_id = models.CharField(max_length=128)
    create_time = models.DateField()

    class Meta:
        managed = False
        db_table = 'app_idc'


class AppIdcGroups(models.Model):
    idc = models.ForeignKey(AppIdc, models.DO_NOTHING)
    group = models.ForeignKey('AuthGroup', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'app_idc_groups'
        unique_together = (('idc', 'group'),)


class AppMaintainlog(models.Model):
    maintain_type = models.CharField(max_length=32)
    hard_type = models.CharField(max_length=16)
    time = models.DateTimeField()
    operator = models.CharField(max_length=16)
    note = models.TextField()
    host = models.ForeignKey(AppHost, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'app_maintainlog'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class BlogBlogpost(models.Model):
    title = models.CharField(max_length=150)
    body = models.TextField()
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'blog_blogpost'


class BlogTestmodel(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'blog_testmodel'


class DataBrowse(models.Model):
    uid = models.IntegerField()
    pid = models.IntegerField()
    btime = models.DateTimeField(blank=True, null=True)

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


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class ProductRecommend(models.Model):
    pid = models.IntegerField()
    rpid = models.IntegerField()
    rating = models.FloatField()

    class Meta:
        managed = False
        db_table = 'product_recommend'


class ReversionRevision(models.Model):
    date_created = models.DateTimeField()
    comment = models.TextField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reversion_revision'


class ReversionVersion(models.Model):
    object_id = models.CharField(max_length=191)
    format = models.CharField(max_length=255)
    serialized_data = models.TextField()
    object_repr = models.TextField()
    content_type = models.ForeignKey(DjangoContentType, models.DO_NOTHING)
    revision = models.ForeignKey(ReversionRevision, models.DO_NOTHING)
    db = models.CharField(max_length=191)

    class Meta:
        managed = False
        db_table = 'reversion_version'
        unique_together = (('db', 'content_type', 'object_id', 'revision'),)


class UserRating(models.Model):
    uid = models.IntegerField()
    pid = models.IntegerField()
    rating = models.FloatField()

    class Meta:
        managed = False
        db_table = 'user_rating'


class UserRecommend(models.Model):
    uid = models.IntegerField()
    pid = models.IntegerField()
    rating = models.FloatField()

    class Meta:
        managed = False
        db_table = 'user_recommend'


class XadminBookmark(models.Model):
    title = models.CharField(max_length=128)
    url_name = models.CharField(max_length=64)
    query = models.CharField(max_length=1000)
    is_share = models.BooleanField()
    content_type = models.ForeignKey(DjangoContentType, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'xadmin_bookmark'


class XadminUsersettings(models.Model):
    key = models.CharField(max_length=256)
    value = models.TextField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'xadmin_usersettings'


class XadminUserwidget(models.Model):
    page_id = models.CharField(max_length=256)
    widget_type = models.CharField(max_length=50)
    value = models.TextField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'xadmin_userwidget'
