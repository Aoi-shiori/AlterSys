from django.shortcuts import render,reverse,redirect
from django.views.generic import View
from django.views.decorators.http import require_POST,require_GET
from utils import resful
from Apps.Alter_Dict.models import Alt_Type,Alt_Database,Alt_Hospital,CtDepartment
from .forms import DB_Dict_Form,AltType_Dict_Form,Hospital_Dict_Form,Hospital_Dict_addForm,AltType_Dict_addForm,DB_Dict_addForm
from  Apps.Alter_management.models import Alter_managment
from Apps.Alter_execute.models import Alter_execute
from django.core.paginator import Paginator
from django.db.models import Q
from urllib import parse
from _datetime import datetime
from Apps.Alterauth.decorators import Alter_login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
# Create your views here.


# * @函数名: DB_Dict_Views
# * @功能描述: 数据库类型数据视图，用于前端页面数据展示
# * @作者: 郭军
# * @时间: 2019-6-28 09:10:31
# * @最后编辑时间: 2019-8-28 09:57:23
# * @最后编辑者: 郭军
@method_decorator(Alter_login_required,name='dispatch')
# @method_decorator(permission_required('Alter_Dict.change_alt_database',login_url='/alter/index/'),name="dispatch")
# @method_decorator(permission_required('Alter_Dict.change_alt_database',login_url='/'),name="dispatch")
class Database_dict_Views(View):
    def get(self,request):
        # for Databases in Alt_Database.objects.all():
        #     classifycount=Alter_managment.objects.filter(dbnumber=Databases.pk).count()
        #     Alt_Database.objects.filter(pk=Databases.pk).update(classifycount=classifycount)

        page = int(request.GET.get('p', 1))  # 获当前页数,并转换成整形，没有传默认为1

        cxtj = request.GET.get('cxtj')  # 获取查询条件录入信息

        Databases = Alt_Database.objects.all()#从模型中找出所有的数据

        if cxtj:#查询条件判断
            #多条件模糊查询匹配，满足一个即可返回，用到Q对象格式如下
            Databases=Databases.filter(Q(Database__icontains=cxtj)|Q(id__icontains=cxtj))


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
        return render(request, 'Alter_Dictionaries/Dict_Database.html', context=context)

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


# * @函数名: Add_DB_Dict
# * @功能描述: 数据库类型添加
# * @作者: 郭军
# * @时间: 2019-6-28 09:10:31
# * @最后编辑时间: 2019-9-9 16:54:09
# * @最后编辑者: 郭军
@Alter_login_required
def Add_DB_Dict(request):
    #dbname = request.POST.get('Database')
    if request.user.has_perm('Alter_Dict.change_alt_database'):
        form =DB_Dict_addForm(request.POST)
        if form.is_valid():
            dbname = form.cleaned_data.get('Database')
            exists= Alt_Database.objects.filter(dbname=dbname).exists()
            if not exists:
                Alt_Database.objects.create(dbname=dbname,modifier=request.user.username)
                return resful.OK()
            else:
                return resful.params_error(message='该数据库分类名称已经存在')
        else:
            return resful.params_error(form.get_error())
    else:
        return resful.unauth(message='您没有添加数据库类型字典的权限！')
# * @函数名: Edit_DB_Dict
# * @功能描述: 编辑数据库类型
# * @作者: 郭军
# * @时间: 2019-6-28 09:10:31
# * @最后编辑时间: 2019-9-9 16:49:09
# * @最后编辑者: 郭军
@Alter_login_required
def Edit_DB_Dict(request):
    if request.user.has_perm('Alter_Dict.change_alt_database'):
        form = DB_Dict_Form(request.POST)
        if form.is_valid():
            pk=form.cleaned_data.get('pk')
            Database=form.cleaned_data.get('Database')
            try:
                Alt_Database.objects.filter(pk=pk).update(dbname=Database, modifier=request.user.username,modifytime=datetime.now())
                return resful.OK()
            except:
                return resful.params_error(message="该分类不存在！")
        else:
            return resful.params_error(form.get_error())
    else:
        return resful.unauth(message='您没有编辑数据库类型字典的权限！')


# * @函数名: Del_DB_Dict
# * @功能描述: 删除数据库类型
# * @作者: 郭军
# * @时间: 2019-6-28 09:10:31
# * @最后编辑时间: 2019-9-9 16:48:12
# * @最后编辑者: 郭军
@Alter_login_required
def Del_DB_Dict(request):
    if request.user.has_perm('Alter_Dict.change_alt_database'):
        pk = request.POST.get("pk")
        try:
            Alt_Database.objects.filter(pk=pk).delete()
            return resful.OK()
        except:
            return resful.params_error(message="该分类不存在！")
    else:
        return resful.unauth(message='您没有删除数据库类型字典的权限！')


# * @函数名: AltType_Dict_view
# * @功能描述: 变更类型数据视图，用于前端页面数据展示
# * @作者: 郭军
# * @时间: 2019-6-28 09:10:31
# * @最后编辑时间: 2019-9-9 16:45:56
# * @最后编辑者: 郭军
@method_decorator(Alter_login_required,name="dispatch")
# @method_decorator(permission_required('Alter_Dict.change_alt_type',login_url='/alter/index/'),name="dispatch")
class AltType_Dict_view(View):
    def get(self,request):
        # for AltTypes in Alt_Type.objects.all():
        #     classifycount = Alter_managment.objects.filter(altertypenumber_id=AltTypes.pk).count()
        #     Alt_Type.objects.filter(pk=AltTypes.pk).update(classifycount=classifycount)


        page = int(request.GET.get('p', 1))  # 获当前页数,并转换成整形，没有传默认为1
        cxtj = request.GET.get('cxtj')  # 获取查询条件录入信息

        AltTypes=Alt_Type.objects.all()
        if cxtj:
            AltTypes =AltTypes.filter(Q(AltType__icontains=cxtj))

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




# * @函数名: Add_AltType_Dict
# * @功能描述: 添加变更类型
# * @作者: 郭军
# * @时间: 2019-6-28 09:10:31
# * @最后编辑时间: 2019-9-9 16:46:08
# * @最后编辑者: 郭军
@Alter_login_required

def Add_AltType_Dict(request):
    if request.user.has_perm('Alter_Dict.change_alt_type'):
        #altertypename = request.POST.get('AltType')
        form = AltType_Dict_addForm(request.POST)
        if form.is_valid():
            altertypename = form.cleaned_data.get('AltType')

            exists=Alt_Type.objects.filter(altertypename=altertypename).exists()
            if not exists:
                Alt_Type.objects.create(altertypename=altertypename,modifier=request.user.username,modifytime=datetime.now())
                return resful.OK()
            else:
                return resful.params_error("该类型已经存在！")
        else:
            return resful.params_error(form.get_error())
    else:
        return resful.unauth(message="您没有添加变更类型字典的权限！")


# * @函数名: Edit_AltType_Dict
# * @功能描述: 编辑变更类型
# * @作者: 郭军
# * @时间: 2019-6-28 09:10:31
# * @最后编辑时间: 2019-9-9 16:27:59
# * @最后编辑者: 郭军
@Alter_login_required
def Edit_AltType_Dict(request):
    if request.user.has_perm('Alter_Dict.change_alt_type'):
        form=AltType_Dict_Form(request.POST)
        if form.is_valid():
            pk =form.cleaned_data.get("pk")
            altertypename=form.cleaned_data.get('altertypename')
            try:
                Alt_Type.objects.filter(pk=pk).update(altertypename=altertypename,modifier=request.user.username,modifytime=datetime.now())
                return resful.OK()
            except:
                return resful.params_error(message="该类型不存在！")
        else:
            return resful.params_error(form.get_error())
    else:
        return resful.unauth(message='您没有编辑字典的权限！')

# * @函数名: Del_AltType_Dict
# * @功能描述: 删除变更类型
# * @作者: 郭军
# * @时间: 2019-6-28 09:10:31
# * @最后编辑时间: 2019-9-9 16:27:51
# * @最后编辑者: 郭军
@Alter_login_required
def Del_AltType_Dict(request):
    if request.user.has_perm('Alter_Dict.change_alt_type'):
        pk=request.POST.get('pk')
        try:
            Alt_Type.objects.filter(pk=pk).delete()
            return resful.OK()
        except:
            return resful.params_error(message="该变更类型不存在！")
    else:
        return resful.unauth(message='您没有删除字典的权限！')




# * @函数名: Hospital_Dict_view
# * @功能描述: 医院字典数据视图，用于前端页面数据展示
# * @作者: 郭军
# * @时间: 2019-6-28 09:10:31
# * @最后编辑时间: 2019-9-9 16:27:12
# * @最后编辑者: 郭军
@method_decorator(Alter_login_required,name="dispatch") #装饰器登陆用户才可以访问
# @method_decorator(permission_required('Alter_Dict.change_alt_hospital',login_url='/alter/index/'),name="dispatch") #装饰器拥有指定权限才能访问，否则重定向到主页！
class Hospital_Dict_view(View):
    def get(self,request):
        # for Althospital in Alt_Hospital.objects.all():
        #     classifycount = Alter_execute.objects.filter(hospital_id=Althospital.pk).count()
        #     Alt_Hospital.objects.filter(pk=Althospital.pk).update(classifycount=classifycount)


        page = int(request.GET.get('p', 1))  # 获当前页数,并转换成整形，没有传默认为1
        cxtj = request.GET.get('cxtj')  # 获取查询条件录入信息

        Althospitals=Alt_Hospital.objects.all()
        #Althospitals=CtDepartment.objects.using('ct_department').all()


        if cxtj:
            Althospitals =Althospitals.filter(Q(Hospital__icontains=cxtj))

        paginator = Paginator(Althospitals, 5)  # 通过调用分页方法，对数据进行分页，表示每2条数据分一页
        if paginator.num_pages < page:#用于当前页数据全部删除 发送请求导致查不到数据的错误
            page = paginator.num_pages

        page_obj = paginator.page(page)  # 获取总页数
        context_date = self.get_pagination_data(paginator, page_obj)  # 调用分页函数获取到页码
        context = {
            'HospitalDatas': page_obj.object_list,
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
        return render(request, 'Alter_Dictionaries/Dict_Hospital.html',context=context)

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

# * @函数名: department_Dict_view
# * @功能描述: 雲庫的医院数据视图，用于前端页面数据展示
# * @作者: 郭军
# * @时间: 2019-6-28 09:10:31
# * @最后编辑时间: 2019-9-9 16:27:12
# * @最后编辑者: 郭军
@method_decorator(Alter_login_required,name="dispatch") #装饰器登陆用户才可以访问
# @method_decorator(permission_required('Alter_Dict.change_alt_hospital',login_url='/alter/index/'),name="dispatch") #装饰器拥有指定权限才能访问，否则重定向到主页！
class department_Dict_view(View):
    def get(self,request):
        # for Althospital in Alt_Hospital.objects.all():
        #     classifycount = Alter_execute.objects.filter(hospital_id=Althospital.pk).count()
        #     Alt_Hospital.objects.filter(pk=Althospital.pk).update(classifycount=classifycount)


        page = int(request.GET.get('p', 1))  # 获当前页数,并转换成整形，没有传默认为1
        cxtj = request.GET.get('cxtj')  # 获取查询条件录入信息

        #Althospitals=Alt_Hospital.objects.all()
        Departments=CtDepartment.objects.using('ct_department').all()


        if cxtj:
            Departments =Departments.filter(Q(dept_name__icontains=cxtj)|Q(dept_id=cxtj))

        paginator = Paginator(Departments, 7)  # 通过调用分页方法，对数据进行分页，表示每2条数据分一页
        if paginator.num_pages < page:#用于当前页数据全部删除 发送请求导致查不到数据的错误
            page = paginator.num_pages

        page_obj = paginator.page(page)  # 获取总页数
        context_date = self.get_pagination_data(paginator, page_obj)  # 调用分页函数获取到页码
        context = {
            'departments': page_obj.object_list,
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
        return render(request, 'Alter_Dictionaries/Dict_department.html',context=context)

    def get_pagination_data(self, paginator, page_obj, around_count=7):
        current_page = page_obj.number
        num_pages = paginator.num_pages

        left_has_more = False
        right_has_more = False

        if current_page <= around_count + 7:
            left_pages = range(1, current_page)
        else:
            left_has_more = True
            left_pages = range(current_page - around_count, current_page)

        if current_page >= num_pages - around_count - 1:
            right_pages = range(current_page + 1, num_pages + 1)
        else:
            right_has_more = True
            right_pages = range(current_page + 1, current_page + around_count + 1)

        start_num = (current_page - 1) * around_count

        return {
            # left_pages：代表的是当前这页的左边的页的页码
            'left_pages': left_pages,
            # right_pages：代表的是当前这页的右边的页的页码
            'right_pages': right_pages,
            'current_page': current_page,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'num_pages': num_pages,
            'start_num':start_num,
        }



# * @函数名: Add_hospital_Dict
# * @功能描述: 添加医院字典
# * @作者: 郭军
# * @时间: 2019-8-28 09:10:31
# * @最后编辑时间: 2019-9-9 16:27:20
# * @最后编辑者: 郭军
@Alter_login_required
def Add_hospital_Dict(request):
    if request.user.has_perm('Alter_Dict.change_alt_hospital'):
        # hospitalname=request.POST.get('hospital')
        form = Hospital_Dict_addForm(request.POST)
        if form.is_valid():
            hospitalname = form.cleaned_data.get('hospital')
            exists=Alt_Hospital.objects.filter(hospitalname=hospitalname).exists()
            if not exists:
                Alt_Hospital.objects.create(hospitalname=hospitalname,modifier=request.user.username)
                return resful.OK()
            else:
                return resful.params_error("该医院已经存在！")
        else:
            return resful.params_error(form.get_error())
    else:
        return resful.unauth(message='您没有添加医院字典权限！')
# * @函数名: Edit_hospital_Dict
# * @功能描述: 编辑医院字典
# * @作者: 郭军
# * @时间: 2019-8-28 09:10:31
# * @最后编辑时间: 2019-9-9 16:27:25
# * @最后编辑者: 郭军
@Alter_login_required
def Edit_hospital_Dict(request):
    if request.user.has_perm('Alter_Dict.change_alt_hospital'):
        form=Hospital_Dict_Form(request.POST)
        if form.is_valid():
            pk =form.cleaned_data.get("pk")
            hospitalname=form.cleaned_data.get('Hospital')
            try:
                Alt_Hospital.objects.filter(pk=pk).update(hospitalname=hospitalname, modifier=request.user.username, modifytime=datetime.now())
                return resful.OK()
            except:
                return resful.params_error(message="该医院不存在！")
        else:
            return resful.params_error(form.get_error())
    else:
        return resful.unauth(message='您没有编辑字典的权限！')

# * @函数名: Del_hospital_Dict
# * @功能描述: 删除医院字典
# * @作者: 郭军
# * @时间: 2019-8-28 09:10:31
# * @最后编辑时间: 2019-9-9 16:27:33
# * @最后编辑者: 郭军
@Alter_login_required
def Del_hospital_Dict(request):
    if request.user.has_perm('Alter_Dict.change_alt_hospital'):
        pk=request.POST.get('pk')
        try:
            Alt_Hospital.objects.filter(pk=pk).delete()
            return resful.OK()
        except:
            return resful.params_error(message="该医院不存在！")
    else:
        return resful.unauth(message='您没有删除医院字典的权限！')