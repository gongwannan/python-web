#!/user/bin/env/python
# -*- coding:utf-8 -*_
#作者:gongwannan
from django.conf.urls import url
from django.urls import path
from login import views

urlpatterns =[


    path('register/',views.register),
    path('logout/',views.logout),
    path('confirm/', views.user_confirm),
    path('test/',views.test),
    path('usermessage/', views.usermessage)

]