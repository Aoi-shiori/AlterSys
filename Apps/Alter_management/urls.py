#encoding:utf-8
from django.urls import path
from . import views
app_name ='mangement'

urlpatterns = [
    path('',views.index,name ='index'),
    path('login/',views.login,name='login'),
]