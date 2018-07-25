from django.conf.urls import url

from myApp import views

urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^show/$', views.show, name='show'),
    url(r'^more/(?P<cid>\d+)/(?P<sid>\d+)/$', views.more, name='more'),

]