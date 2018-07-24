from django.conf.urls import url

from myAdmin import views

urlpatterns = [
    url(r'^product_list$', views.index, name='index'),
    url(r'^product_detail$', views.product_detail, name='detail'),
    url(r'^login/$', views.login, name='login'),
    url(r'^modify/$', views.modify, name='modify')
]
