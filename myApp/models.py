from django.db import models

from user.models import User, UserAddress


class Category(models.Model):
    name = models.CharField(max_length=50)  # 分类名称

    class Meta():
        db_table = 'ttsx_category'


class ChildCategory(models.Model):
    name = models.CharField(max_length=50)  # 子分类名称
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)  # 关联分类

    class Meta():
        db_table = 'ttsx_childcategory'


class Goods(models.Model):
    icon = models.ImageField(upload_to='upload')  # 图片
    name = models.CharField(max_length=20)  # 名称
    price = models.FloatField(default=0)  # 价格
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # 分类
    childcategory = models.ForeignKey(ChildCategory, on_delete=models.CASCADE)  # 子分类
    specifics = models.CharField(max_length=100)  # 规格
    introducte = models.CharField(max_length=255)  # 简介
    Popularity = models.IntegerField(default=0)  # 人气

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
    goods = models.ForeignKey(Goods,on_delete=models.DO_NOTHING)  # 关联的商品
    order = models.ForeignKey(Order, on_delete=models.CASCADE)  # 关联的订单
    goods_num = models.IntegerField(default=1)  # 商品的个数

    class Meta:
        db_table = 'ttsx_order_goods'
