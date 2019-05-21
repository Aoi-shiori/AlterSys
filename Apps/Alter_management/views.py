from django.shortcuts import render,redirect
from django.views.generic import View
#导入只接受GET请求和POST请求的装饰器
from django.views.decorators.http import require_GET,require_POST
#导入form验证用的表单
from .forms import Alterform
#导入Alter_manage的模型
from Apps.Alter_management.models import Alter_managment
#
from utils import resful


# Create your views here.

def login(request):
    return render(request,'Alter_management/login.html')

def index_manage(request):
    return render(request,"Alter_management/index.html")

@require_GET#只接受GET请求
# class Alter_manager_view(View):#变更管理页面，包含数据
def Alter_manager_view (request):
        Alterd_datas=Alter_managment.objects.all()
        context={
            'Alterd_datas':Alterd_datas
        }
        return render(request,"Alter_management/Alter.html",context=context)




@require_POST#只接受POST的请求
def add_Alter_manager(request):#添加变更内容
    form = Alterform(request.POST)
    #如果验证成功
    if form.is_valid():
        AlterType = form.cleaned_data.get('AlterType')
        AssociatedNumber = form.cleaned_data.get('AssociatedNumber')
        Datebase = form.cleaned_data.get('Datebase')
        AlterContent=form.cleaned_data.get('AlterContent')
        Informant=form.cleaned_data.get('Informant')

        #判断变更内容在库中是否存在
        exists=Alter_managment.objects.filter(AlterContent=AlterContent).exists()
        if not exists:
            Alter_managment.objects.create(AlterType=AlterType, AssociatedNumber=AssociatedNumber, Datebase=Datebase,
                                           Informant=Informant)
            return resful.OK()
        else:
            return resful.params_error(message="该变更交内容已经存在")



class Alter_add_view(View):#旧的变更提交页面
    def get(self,request):
        return render(request,"Alter_management/Alter_add.html")