#encoding:utf-8
from django.urls import path
from . import views
app_name ='Execute'

urlpatterns = [
    path('Alter_execute',views.Alter_Execute_view.as_view(),name ='Alter_execute'),
    path('download/',views.download,name="export_download"),
    path('alter_execute_history/',views.alter_execute_history_view.as_view(),name="alter_execute_history"),
    path('test_select/',views.test_select,name="test_select"),
    path('export_alt_datas_view/',views.export_alt_datas_view.as_view(),name="export_alt_datas_view"),
    path('new_file_down/',views.new_file_down,name="new_file_down"),
    path('test/',views.test,name="test"),
]