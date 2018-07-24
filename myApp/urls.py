from django.conf.urls import url

from myApp import views

urlpatterns = [
    url('index', views.index, name='index')
]