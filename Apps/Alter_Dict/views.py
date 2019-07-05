from django.shortcuts import render,reverse,redirect
from django.views.generic import View
from django.views.decorators.http import require_POST,require_GET
from utils import resful
from Apps.Alter_Dict.models import AltType,DBname
from .forms import DB_Dict_Form,AltType_Dict_Form
from  Apps.Alter_management.models import Alter_managment
from django.core.paginator import Paginator
from django.db.models import Q
from urllib import parse
# Create your views here.

#数据库类型数据视图
class DB_Dict_Views(View):
    def get(self,request):
        for Databases in DBname.objects.all():
            counts=Alter_managment.objects.filter(Database=Databases.pk).count()
            DBname.objects.filter(pk=Databases.pk).update(counts=counts)

        page = int(request.GET.get('p', 1))  # 获当前页数,并转换成整形，没有传默认为1

        cxtj = request.GET.get('cxtj')  # 获取查询条件录入信息

        Databases = DBname.objects.all()#从模型中找出所有的数据

        if cxtj:#查询条件判断
            #多条件模糊查询匹配，满足一个即可返回，用到Q对象格式如下
            Databases=Databases.filter(Q(Database__icontains=cxtj)|Q(id__icontains=cxtj)|Q(counts__icontains=cxtj))


        paginator = Paginator(Databases, 5)  # 通过调用分页方法，对数据进行分页，表示每2条数据分一页
        if paginator.num_pages < page:
            page = paginator.num_pages

        page_obj = paginator.page(page)  # 获取总页数
        context_date = self.get_pagination_data(paginator, page_obj)  # 调用分页函数获取到页码
        context = {
            'Databases': page_obj.object_list,
            'page_obj': page_obj,  # 将分了多少页的数据全部传过去
            'paginator': page,  # 当前页数据
            'cxtj': cxtj,
            'url_query': '&' + parse.urlencode({
                 'cxtj': cxtj or '',
            })  # 用于拼接url,让页面在查询后进行翻页，任然保留查询条件

        }  # 返回包含分页信息的数据

        context.update(context_date)  # 将分页数据更新到context,返回返回给页面

        # context={
        #     'Databases':Databases
        # }
        return render(request, 'Alter_Dictionaries/Dict_DB.html', context=context)

        # 获取和分页功能

    def get_pagination_data(self, paginator, page_obj, around_count=2):
        current_page = page_obj.number
        num_pages = paginator.num_pages

        left_has_more = False
        right_has_more = False

        if current_page <= around_count + 2:
            left_pages = range(1, current_page)
        else:
            left_has_more = True
            left_pages = range(current_page - around_count, current_page)

        if current_page >= num_pages - around_count - 1:
            right_pages = range(current_page + 1, num_pages + 1)
        else:
            right_has_more = True
            right_pages = range(current_page + 1, current_page + around_count + 1)

        return {
            # left_pages：代表的是当前这页的左边的页的页码
            'left_pages': left_pages,
            # right_pages：代表的是当前这页的右边的页的页码
            'right_pages': right_pages,
            'current_page': current_page,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'num_pages': num_pages
        }


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
        for AltTypes in AltType.objects.all():
            counts = Alter_managment.objects.filter(AltType=AltTypes.pk).count()
            AltType.objects.filter(pk=AltTypes.pk).update(counts=counts)


        page = int(request.GET.get('p', 1))  # 获当前页数,并转换成整形，没有传默认为1
        cxtj = request.GET.get('cxtj')  # 获取查询条件录入信息

        AltTypes=AltType.objects.all()
        if cxtj:
            AltTypes =AltTypes.filter(Q(AltType__icontains=cxtj)|Q(counts__icontains=cxtj))

        paginator = Paginator(AltTypes, 5)  # 通过调用分页方法，对数据进行分页，表示每2条数据分一页
        if paginator.num_pages < page:#用于当前页数据全部删除 发送请求导致查不到数据的错误
            page = paginator.num_pages

        page_obj = paginator.page(page)  # 获取总页数
        context_date = self.get_pagination_data(paginator, page_obj)  # 调用分页函数获取到页码
        context = {
            'AltTypes': page_obj.object_list,
            'page_obj': page_obj,  # 将分了多少页的数据全部传过去
            'paginator': page,  # 当前页数据
            'cxtj': cxtj,
            'url_query': '&' + parse.urlencode({
               'cxtj': cxtj or '',
            })  # 用于拼接url,让页面在查询后进行翻页，任然保留查询条件

        }  # 返回包含分页信息的数据

        context.update(context_date)  # 将分页数据更新到context,返回返回给页面



        # context={
        #     'AltTypes':alttype
        # }
        return render(request, 'Alter_Dictionaries/Dict_AltType.html',context=context)

    def get_pagination_data(self, paginator, page_obj, around_count=2):
        current_page = page_obj.number
        num_pages = paginator.num_pages

        left_has_more = False
        right_has_more = False

        if current_page <= around_count + 2:
            left_pages = range(1, current_page)
        else:
            left_has_more = True
            left_pages = range(current_page - around_count, current_page)

        if current_page >= num_pages - around_count - 1:
            right_pages = range(current_page + 1, num_pages + 1)
        else:
            right_has_more = True
            right_pages = range(current_page + 1, current_page + around_count + 1)

        return {
            # left_pages：代表的是当前这页的左边的页的页码
            'left_pages': left_pages,
            # right_pages：代表的是当前这页的右边的页的页码
            'right_pages': right_pages,
            'current_page': current_page,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'num_pages': num_pages
        }





#添加变更类型
def Add_AltType_Dict(request):
    altType=request.POST.get('AltType')
    exists=AltType.objects.filter(AltType=altType).exists()
    if not exists:
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