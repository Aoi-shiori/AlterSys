#encoding:utf-8
from django.urls import path
from . import views
app_name ='mangement'

urlpatterns = [
    path('',views.login,name ='index'),
    path('login/',views.login,name='login'),
    path('index/',views.index_manage,name='index_manage'),
    path('Alter_manager/',views.Alter_manager_view.as_view(),name='Alter_manager'),
]