from django.shortcuts import render
from django.views.generic import View
# Create your views here.

def login(request):
    return render(request,'Alter_management/login.html')

def index_manage(request):
    return render(request,"Alter_management/index.html")

class Alter_manager_view(View):
    def get (self,request):
        return render(request,"Alter_management/Alter.html")
