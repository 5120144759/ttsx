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

]