from django.conf.urls import url

from myApp import views

urlpatterns = [
    # 首页
    url(r'^index/$', views.index, name='index'),
    # 跳转
    url(r'^show/$', views.show, name='show'),
    # 商品页面
    url(r'^more/(?P<cid>\d+)/(?P<sid>\d+)/$', views.more, name='more'),
    # 详情页面
    url(r'^detail/(?P<cid>\d+)/(?P<gid>\d+)$', views.detail, name='detail'),
    # 添加购物车
    url(r'^add_cart/$', views.addCart, name='addCart'),
    # 刷新购物车中商品数量
    url(r'^cart_num/$', views.cartNum, name='cart_num'),
    # 详情页面添加购物车
    url(r'^detail_add_cart/$', views.detailAddCart, name='detail_add_cart'),
]