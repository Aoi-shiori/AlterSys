#encoding:utf-8
from django.urls import path
from . import views
app_name ='Dict'

urlpatterns = [
    path('DB_Dict',views.DB_Dict_Views.as_view(),name ='DB_View'),
    path('Add_DB_Dict/',views.Add_DB_Dict,name="Add_DB_Dict"),
    path('Del_DB_Dict/',views.Del_DB_Dict,name="Del_DB_Dict"),
    path('Edit_DB_Dict/',views.Edit_DB_Dict,name="Edit_DB_Dict"),
    path('DB_AltType',views.AltType_Dict_view.as_view(),name="AltType_View"),
    path('Add_AltType_Dict/',views.Add_AltType_Dict,name="Add_AltType_Dict"),
    path('Edit_AltType_Dict/',views.Edit_AltType_Dict,name="Edit_AltType_Dict"),
    path('Del_AltType_Dict/',views.Del_AltType_Dict,name="Del_AltType_Dict"),
]