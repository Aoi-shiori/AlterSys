from django.shortcuts import render,redirect
from django.views.generic import View
#导入只接受GET请求和POST请求的装饰器
from django.views.decorators.http import require_GET,require_POST
#导入form验证用的表单
from .forms import Alterform,EditAlterform
#导入Alter_manage的模型
from Apps.Alter_management.models import Alter_managment
#导入我们重构的resful文件，用于返回结果代码和消息，详细可以看resful.py文件
from utils import resful


# Create your views here.

def login(request):
    return render(request,'Alter_management/login.html')

def index_manage(request):
    return render(request,"Alter_management/index.html")

@require_GET#只接受GET请求
# class Alter_manager_view(View):#变更管理页面，返回数据
def Alter_manager_view (request):
        Alterd_datas=Alter_managment.objects.all()
        context={
            'Alterd_datas':Alterd_datas
        }
        return render(request,"Alter_management/Alter.html",context=context)

def edit_Alter_manager(request):
    form =EditAlterform(request.POST)
    if form.is_valid():
        AlterID=form.cleaned_data.get("prekey")#变更ID
        AlterType = form.cleaned_data.get("AlterType")  # '关联类型'#
        AssociatedNumber =form.cleaned_data.get("AssociatedNumber")  # '关联编号'#
        Datebase = form.cleaned_data.get("Datebase")  # '数据库'#
        AlterContent =form.cleaned_data.get("AlterContent")  # 变更内容
        Informant = form.cleaned_data.get("Informant")  # '填报人',
        try:
            Alter_managment.objects.filter(AlterID=AlterID).update(AlterType=AlterType, AssociatedNumber=AssociatedNumber, Datebase=Datebase, AlterContent=AlterContent, Informant=Informant)
            return resful.OK()
        except:
            return resful.params_error(message=form.get_error())
@require_POST
def delete_Alter_manager(request):
    AlterID=request.POST.get("AlterID")
    try:
        Alter_managment.objects.filter(AlterID=AlterID).delete()
        return resful.OK()
    except:
        return resful.params_error(message="该变更不存在")

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
            Alter_managment.objects.create(AlterType=AlterType, AssociatedNumber=AssociatedNumber, Datebase=Datebase,AlterContent=AlterContent,
                                           Informant=Informant)
            return resful.OK()
        else:
            return resful.params_error(message="该变更交内容已经存在")



class Alter_add_view(View):#旧的变更提交页面
    def get(self,request):
        return render(request,"Alter_management/Alter_add.html")