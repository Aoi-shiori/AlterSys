#encoding:utf-8
from django.urls import path
from . import views
app_name ='Execute'

urlpatterns = [
    path('Alter_execute',views.Alter_Execute_view.as_view(),name ='Alter_execute'),
    path('add_Alter_Execute/',views.add_Alter_Execute,name="add_Alter_Execute"),

]