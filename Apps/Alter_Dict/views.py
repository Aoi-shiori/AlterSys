from django.shortcuts import render,reverse,redirect
from django.views.generic import View
from django.views.decorators.http import require_POST,require_GET
from utils import resful
from Apps.Alter_Dict.models import AltType,DBname
from .forms import DB_Dict_Form,AltType_Dict_Form
# Create your views here.

#数据库类型数据视图
class DB_Dict_Views(View):
    def get(self,request):
        Databases = DBname.objects.all()
        context={
            'Databases':Databases
        }
        return render(request, 'Alter_Dictionaries/Dict_DB.html', context=context)

#数据库类型添加
def Add_DB_Dict(request):
    Database =request.POST.get('Database')
    exists= DBname.objects.filter(Database=Database).exists()
    if not exists:
        DBname.objects.create(Database=Database)
        return resful.OK()
    else:
        return resful.params_error(message='该数据库分类名称已经存在')
#编辑数据库类型
def Edit_DB_Dict(request):
    form = DB_Dict_Form(request.POST)
    if form.is_valid():
        pk=form.cleaned_data.get('pk')
        Database=form.cleaned_data.get('Database')
        try:
            DBname.objects.filter(pk=pk).update(Database=Database)
            return resful.OK()
        except:
            return resful.params_error(message="该分类不存在！")
    else:
        return resful.params_error(form.get_error())
#删除数据库类型
def Del_DB_Dict(request):
    pk = request.POST.get("pk")
    try:
        DBname.objects.filter(pk=pk).delete()
        return resful.OK()
    except:
        return resful.params_error(message="该分类不存在！")

#变更类型数据视图
class AltType_Dict_view(View):
    def get(self,request):
        alttype=AltType.objects.all()
        context={
            'AltType':alttype
        }
        return render(request, 'Alter_Dictionaries/Dict_AltType.html',context=context)

#添加变更类型
def Add_AltType_Dict(request):
    altType=request.GET.get('AltType')
    exists=AltType.objects.filter(AltType=altType).exists()
    if not exists():
        AltType.objects.create(AltType=altType)
        return resful.OK()
    else:
        return resful.params_error("该类型已经存在！")

#编辑变更类型
def Edit_AltType_Dict(request):
    form=AltType_Dict_Form(request.POST)
    if form.is_valid():
        pk =form.cleaned_data.get("pk")
        altType=form.cleaned_data.get('AltType')
        try:
            AltType.objects.filter(pk=pk).update(AltType=altType)
            return resful.OK()
        except:
            return resful.params_error(message="该类型不存在！")
    else:
        return resful.params_error(form.get_error())

#删除变更类型
def Del_AltType_Dict(request):
    pk=request.POST.get('pk')
    try:
        AltType.objects.filter(pk=pk).delete()
        return resful.OK()
    except:
        return resful.params_error(message="该变更类型不存在！")