"""AlterSys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path,include
from Apps.Alter_management import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.login),
    path('alter/', include('Apps.Alter_management.urls',namespace='management')),
    path('account/', include("Apps.Alterauth.urls",namespace="Alterauth")),
    path('execute/',include("Apps.Alter_execute.urls",namespace='Execute'))
]
