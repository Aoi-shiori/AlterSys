#encoding:utf-8
from django.urls import path
from . import views
app_name ='management'

urlpatterns = [
    path('',views.login,name ='index'),
    path('login/',views.login,name='login'),
    path('index/',views.index_manage,name='index_manage'),
    path('Alter_manager/',views.Alter_manager_newview.as_view(),name='Alter_manager'),
    path('add_Alter_manager/', views.add_Alter_managerView.as_view(),name='add_Alter_manager'),
    path('edit_Alter_manager/',views.edit_Alter_manager,name='edit_Alter_manager'),
    path('delete_Alter_manager/',views.delete_Alter_manager,name='delete_Alter_manager'),
    path('Alter_deatil/<id>',views.Alter_detail,name='Alter_deatil'),
    path('Review_Alter_manager/',views.Review_Alter_manager,name="Review_Alter_manager"),
    path('test_review/',views.test_review,name="test_review"),

]