#encoding:utf-8
from django.urls import path
from . import views
app_name ='Execute'

urlpatterns = [
    path('Alter_execute',views.Alter_Execute_view.as_view(),name ='Alter_execute'),
    path('add_Alter_Execute/',views.add_Alter_Execute,name="add_Alter_Execute"),
    path('delete_Alter_Execute/',views.delete_Alter_Execute,name="delete_Alter_Execute"),
    path('execute_Alter_Execute/',views.execute_Alter_Execute,name="execute_Alter_Execute"),
]