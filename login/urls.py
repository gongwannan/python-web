#!/user/bin/env/python
# -*- coding:utf-8 -*_
# 作者:gongwannan
from django.conf.urls import url
from django.urls import path
from login import views

urlpatterns = [

    path('register/', views.register),
    path('logout/', views.logout),
    path('confirm/', views.user_confirm),
    path('test/', views.test),
    path('usermessage/', views.usermessage),
    path('about/', views.about),
    path('geren/', views.geren),
    path('shoucang/', views.shoucang),
    path('guanzhu/', views.guanzhu),
    path('fensi/', views.fensi),
    path('zhanghao/', views.zhanghao),
    path('mima/', views.mima),
    path('youxiang/', views.youxiang),
]
