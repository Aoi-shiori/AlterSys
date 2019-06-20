from django.urls import path,include
from .import views

app_name = "Alterauth"
urlpatterns = [
        path('login/', views.login_view, name='login'),
        path('logout/',views.logout_view,name='logout'),
        #员工管理
        path('staffs/',views.staff_view,name='staffs'),
        path('add_staff/',views.AddStaff_view.as_view(),name='add_staff'),

]