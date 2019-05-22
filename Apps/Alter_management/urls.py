#encoding:utf-8
from django.urls import path
from . import views
app_name ='mangement'

urlpatterns = [
    path('',views.login,name ='index'),
    path('login/',views.login,name='login'),
    path('index/',views.index_manage,name='index_manage'),
    # path('Alter_manager/',views.Alter_manager_view.as_view,name='Alter_manager'),
    path('Alter_manager/',views.Alter_manager_view,name='Alter_manager'),
    path('Alter_add/',views.Alter_add_view.as_view(),name="Alter_add"),
    #添加变更数据
    path('add_Alter_manager/', views.add_Alter_manager,name='add_Alter_manager'),
]