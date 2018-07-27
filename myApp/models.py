from django.db import models

from user.models import User, UserAddress


class Category(models.Model):
    name = models.CharField(max_length=50)  # 分类名称
    icon = models.ImageField(upload_to='upload', null=True) # 分类图片

    class Meta():
        db_table = 'ttsx_category'


class Goods(models.Model):
    icon = models.ImageField(upload_to='upload')  # 图片
    name = models.CharField(max_length=20)  # 名称
    price = models.FloatField(default=0)  # 价格
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # 分类
    specifics = models.CharField(max_length=100)  # 规格s
    introducte = models.CharField(max_length=255)  # 简介
    Popularity = models.BooleanField(default=0)  # 人气

    class Meta():
        db_table = 'ttsx_goods'


class Main(models.Model):
    img = models.CharField(max_length=200)  # 图片
    name = models.CharField(max_length=100)  # 名称

    class Meta:
        abstract = True


class MainWheel(Main):
    # 轮循banner
    class Meta:
        db_table = "ttsx_wheel"


class MainNav(Main):
    # 导航
    class Meta:
        db_table = "ttsx_nav"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 关联用户
    o_num = models.CharField(max_length=64)  # 订单号
    o_status = models.IntegerField(default=0)  # 状态

    class Meta:
        db_table = 'ttsx_order'


class OrderGoodsModel(models.Model):
    goods = models.ForeignKey(Goods, on_delete=models.DO_NOTHING)  # 关联的商品
    order = models.ForeignKey(Order, on_delete=models.CASCADE)  # 关联的订单
    goods_num = models.IntegerField(default=1)  # 商品的个数

    class Meta:
        db_table = 'ttsx_order_goods'


class Cart(models.Model):
    user = models.ForeignKey(User)  # 关联用户
    goods = models.ForeignKey(Goods)  # 关联商品
    c_num = models.IntegerField(default=1)  # 商品的个数
    is_select = models.BooleanField(default=True)  # 是否选择商品

    class Meta:
        db_table = 'ttsx_cart'