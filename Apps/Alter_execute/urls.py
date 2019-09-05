#encoding:utf-8
from django.urls import path
from . import views
app_name ='Execute'

urlpatterns = [
    path('Alter_execute',views.Alter_Execute_view.as_view(),name ='Alter_execute'),
    path('export/',views.export,name="export_Alter_Execute"),
    path('export_new/',views.export_New,name="export_new_Alter_Execute"),
    path('download/',views.download,name="export_download"),
    path('exportAltData/',views.export_alt_data,name="ExportAltData"),
    path('alter_execute_history/',views.alter_execute_history_view.as_view(),name="alter_execute_history"),
    path('test_select/',views.test_select,name="test_select"),
    path('export_alt_datas_view/',views.export_alt_datas_view.as_view(),name="export_alt_datas_view"),
]