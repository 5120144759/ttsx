from django.conf.urls import url

from myAdmin import views

urlpatterns = [
    # 商品列表
    url(r'^product_list$', views.index, name='index'),
    # 商品详情添加
    url(r'^product_detail$', views.product_detail, name='detail'),
    # 后台登录界面
    url(r'^login/$', views.login, name='login'),
    # 商品修改
    url(r'^modify/$', views.modify, name='modify'),
    # 商品删除
    url(r'^delete/$', views.delete, name='delete'),
    # 分类添加
    url(r'^add_category/$', views.addCategoty, name='addcategory'),
    # 订单总览
    url(r'^order_list/$', views.order_list, name='order_list'),
    # 订单详情
    url(r'^order_detail/$', views.order_detail, name='order_detail'),
    # 删除订单
    url(r'^order_delete/$', views.order_delete, name='order_delete'),
]
