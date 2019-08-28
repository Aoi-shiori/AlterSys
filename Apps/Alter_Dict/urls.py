#encoding:utf-8
from django.urls import path
from . import views
app_name ='Dict'

urlpatterns = [
    path('Database_Dict_View',views.Database_dict_Views.as_view(),name ='Database_Dict_View'),
    path('Add_DB_Dict/',views.Add_DB_Dict,name="Add_DB_Dict"),
    path('Del_DB_Dict/',views.Del_DB_Dict,name="Del_DB_Dict"),
    path('Edit_DB_Dict/',views.Edit_DB_Dict,name="Edit_DB_Dict"),
    path('DB_AltType',views.AltType_Dict_view.as_view(),name="AltType_View"),
    path('Add_AltType_Dict/',views.Add_AltType_Dict,name="Add_AltType_Dict"),
    path('Edit_AltType_Dict/',views.Edit_AltType_Dict,name="Edit_AltType_Dict"),
    path('Del_AltType_Dict/',views.Del_AltType_Dict,name="Del_AltType_Dict"),
    path('Hospital_Dict_view/',views.Hospital_Dict_view.as_view(),name="Hospital_Dict_view"),
    path('Add_hospital_Dict/',views.Add_hospital_Dict,name="Add_hospital_Dict"),
    path('Edit_hospital_Dict/',views.Edit_hospital_Dict,name="Edit_hospital_Dict"),
    path('Del_hospital_Dict/',views.Del_hospital_Dict,name="Del_hospital_Dict"),

]