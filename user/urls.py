from django.conf.urls import url

from user import views

urlpatterns = [
    # 登录
    url(r'login/', views.login, name='login'),
    # 注册
    url(r'register/', views.register, name='register'),
    # 登出
    url(r'logout/', views.logout, name='logout'),
    # 用户主页
    url(r'^mine/$', views.mine, name='mine'),
    # 收货地址
    url(r'^address/$', views.address, name='address')
]