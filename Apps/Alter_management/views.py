from django.shortcuts import render,redirect
from django.views.generic import View
#导入只接受GET请求和POST请求的装饰器
from django.views.decorators.http import require_GET,require_POST
#导入form验证用的表单
from .forms import Alterform,EditAlterform,Reviewform
#导入Alter_manage的模型
from Apps.Alter_management.models import Alter_managment
#导入我们重构的resful文件，用于返回结果代码和消息，详细可以看resful.py文件
from utils import resful
#导入分页用的类
from django.core.paginator import Paginator
#导入时间分类
from datetime import datetime
#将时间标记为清醒的时间
from django.utils.timezone import make_aware
#用于模糊查询
from django.db.models import Q
#用于拼接url
from urllib import parse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.contrib.admin.views.decorators import staff_member_required

from django.http import HttpResponse
from .admin import Alter_managment_resources

# Create your views here.


def login(request):
    return render(request,'Alter_management/login.html')

def index_manage(request):
    return render(request,"Alter_management/index.html")

# @require_GET#只接受GET请求
# # class Alter_manager_view(View):#变更管理页面，返回数据
# def Alter_manager_view (request):#变更管理页面，返回数据
#         Alterd_datas=Alter_managment.objects.all()
#         context={
#             'Alterd_datas':Alterd_datas
#         }
#         return render(request,"Alter_management/Alter.html",context=context)


#新变更管理页面
#@staff_member_required(login_url='login')
class Alter_manager_newview(View):#变更管理页面，返回数据
    def get(self,request):
        #request.GET.get获取出来的数据都是字符串类型
        page = int(request.GET.get('p',1))#获当前页数,并转换成整形，没有传默认为1
        start=request.GET.get('start') #获取时间控件开始时间
        end =request.GET.get('end') #获取时间控件结束时间
        cxtj =request.GET.get('cxtj') #获取查询条件录入信息
        #request.GET.get（参数,默认值）
        #这个参数是只有没有传递参数的时候才会使用
        #如果传递了，但是是一个空的字符串，也不会使用，那么可以使用 ('ReviewStatus',0) or 0
        reviewStatus=int(request.GET.get('ReviewStatus',0)) #获取审核状态查询值,因为get到的都是字符串，转换成整形才能在页面中用数值对比

        Alterd_datas = Alter_managment.objects.all()#获取所有数据库的数据

        if start or end:#查询时间判断
            if start:
                start_time=datetime.strptime(start,'%m/%d/%Y')
            else:
                start_time = datetime(year=2019,month=5,day=1)

            if end:
                end_time =datetime.strptime(end,'%m/%d/%Y')
            else:
                end_time=datetime.today()

            Alterd_datas=Alterd_datas.filter(FillTime__range=(make_aware(start_time), make_aware(end_time)))

        if cxtj:#查询条件判断
            #多条件模糊查询匹配，满足一个即可返回，用到Q对象格式如下
            Alterd_datas=Alterd_datas.filter(Q(AlterID__icontains=cxtj)|Q(AlterContent__icontains=cxtj)|Q(AlterType__icontains=cxtj)|Q(Datebase__icontains=cxtj)|Q(Informant__icontains=cxtj)|Q(AssociatedNumber__icontains=cxtj))

        if reviewStatus:#审核状态判断
            Alterd_datas =Alterd_datas.filter(ReviewStatus=reviewStatus)


        paginator = Paginator(Alterd_datas, 2)  # 分页用，表示每2条数据分一页
        page_obj= paginator.page(page)#获取总页数

        context_date =self.get_pagination_data(paginator,page_obj)#调用分页函数获取到页码
        context = {
            'Alterd_datas': page_obj.object_list,
            'page_obj':page_obj,#将分了多少页的数据全部传过去
            'paginator':page,#当前页数据
            'start':start,
            'end':end,
            'cxtj':cxtj,
            'reviewStatus':reviewStatus,
            'url_query': '&'+parse.urlencode({
                'start': start or '',
                'end':end or '',
                'cxtj':cxtj or '',
                'reviewStatus':reviewStatus or '',
            })#用于拼接url,让页面在查询后进行翻页，任然保留查询条件

        }#返回包含分页信息的数据
        
        context.update(context_date)#将分页数据更新到context,返回返回给页面
        return render(request, "Alter_management/Alter.html", context=context)



    #获取和分页功能
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











@require_POST
#@method_decorator(permission_required(perm='alter_managment.change_alter_managment',login_url='/'),name="dispatch")
def edit_Alter_manager(request):#变更内容编辑用
    form =EditAlterform(request.POST)
    if form.is_valid():
        AlterID=form.cleaned_data.get("AlterID")#变更ID
        AlterType = form.cleaned_data.get("AlterType")  # '关联类型'#
        AssociatedNumber =form.cleaned_data.get("AssociatedNumber")  # '关联编号'#
        Datebase = form.cleaned_data.get("Datebase")  # '数据库'#
        AlterContent =form.cleaned_data.get("AlterContent")  # 变更内容
        Alter_managment.objects.filter(AlterID=AlterID).update(AlterType=AlterType, AssociatedNumber=AssociatedNumber, Datebase=Datebase, AlterContent=AlterContent, Informant=request.user.name
,FillTime=datetime.now(),ReviewStatus='0')
        return resful.OK()
    else:
        return resful.params_error(message=form.get_error())

@require_POST
def delete_Alter_manager(request):#变更内容删除用
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

        #判断变更内容在库中是否存在
        exists=Alter_managment.objects.filter(AlterContent=AlterContent).exists()
        if not exists:
            Alter_managment.objects.create(AlterType=AlterType, AssociatedNumber=AssociatedNumber, Datebase=Datebase,AlterContent=AlterContent,
                                           Informant=request.user.name)
            return resful.OK()
        else:

            return resful.params_error(message="该变更内容已经存在!")
    else:
        return resful.params_error(message="验证不通过")

#变更审核
@require_POST
def Review_Alter_manager(request):#变更审核用
    form =Reviewform(request.POST)
    if form.is_valid():
        AlterID = form.cleaned_data.get('AlterID')
        ReviewStatus = form.cleaned_data.get('ReviewStatus')  # '审核状态',
        ReviewContent = form.cleaned_data.get('ReviewContent')  # '审核内容',
        Alter_managment.objects.filter(AlterID=AlterID).update(ReviewStatus=ReviewStatus, ReviewContent=ReviewContent, Reviewer=request.user.name,AuditTime=datetime.now())
        return resful.OK()
    else:
       return resful.params_error(message=form.get_error())





def Alter_detail(request,AlterID):#变更详情页面
        Alterdeatil =Alter_managment.objects.get(AlterID=AlterID)
        context={

            'Alterdeatil':Alterdeatil
        }

        return render(request,"Alter_management/Alter_detail.html",context=context)

class Alter_add_view(View):#旧的变更提交页面
    def get(self,request):
        return render(request,"Alter_management/Alter_add.html")



#导出数据
def export(request):
    alter_managment_resources = Alter_managment_resources()
    queryset = Alter_managment.objects.filter(ReviewStatus='1')
    dataset = alter_managment_resources.export(queryset)
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Alter.csv"'
    return response