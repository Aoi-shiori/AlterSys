from django.shortcuts import render,redirect,reverse
from django.views.generic import View
#导入只接受GET请求和POST请求的装饰器
from django.views.decorators.http import require_GET,require_POST
#导入form验证用的表单
from .forms import Alterform,EditAlterform,Reviewform
#导入Alter_manage的模型
from Apps.Alter_management.models import Alter_managment,Alter_managment_checked
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

from django.http import HttpResponse,JsonResponse
from .admin import Alter_managment_resources
from Apps.Alterauth.decorators import Alter_login_required
#导入数据库字典和变更类型字典
from Apps.Alter_Dict.models import Alt_Database,Alt_Type
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



# * @函数名: Alter_manager_newview
# * @功能描述: 变更管理页面视图
# * @作者: 郭军
# * @时间: 2019-6-30 15:28:19
# * @最后编辑时间: 2019-9-9 16:57:39
# * @最后编辑者: 郭军
#@staff_member_required(login_url='login')
@method_decorator(Alter_login_required,name='dispatch')
# @method_decorator(permission_required('Alter_management.change_alter_managment',login_url='/alter/index/'),name="dispatch")
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
        DatabaseType = int(request.GET.get('DatabaseType',0))
        Alterd_datas = Alter_managment.objects.all()#获取所有数据库的数据
        Databases = Alt_Database.objects.all()
        AltTypes=Alt_Type.objects.all()


        if start or end:#查询时间判断
            if start:
                start_time=datetime.strptime(start,'%Y/%m/%d')
            else:
                start_time = datetime(year=2019,month=5,day=1)#如果是空的 就使用默认值

            if end:
                end_time =datetime.strptime(end,'%Y/%m/%d')
            else:
                end_time=datetime.today()

            Alterd_datas=Alterd_datas.filter(modifytime__range=(make_aware(start_time), make_aware(end_time)))

        if cxtj:#查询条件判断
            #多条件模糊查询匹配，满足一个即可返回，用到Q对象格式如下
            Alterd_datas=Alterd_datas.filter(Q(databaseid=cxtj)|Q(id=cxtj)|Q(altercontent__icontains=cxtj)|Q(altertypeid=cxtj)|Q(modifier__icontains=cxtj)|Q(associatedid__icontains=cxtj))

        if DatabaseType:#数据库类型判断
            Alterd_datas=Alterd_datas.filter(databaseid=DatabaseType)

        if reviewStatus:#审核状态判断
            Alterd_datas =Alterd_datas.filter(reviewstatus=reviewStatus)

        paginator = Paginator(Alterd_datas, 2)  # 分页用，表示每2条数据分一页
        if paginator.num_pages < page:
            page= paginator.num_pages

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
            'DatabaseType':DatabaseType,
            'Databases':Databases,
            'AltTypes':AltTypes,
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




# * @函数名: edit_Alter_manager
# * @功能描述: 编辑变更内容
# * @作者: 郭军
# * @时间: 2019-6-30 15:28:19
# * @最后编辑时间: 2019-9-9 17:00:18
# * @最后编辑者: 郭军
@require_POST
@Alter_login_required
#@method_decorator(permission_required(perm='Alter_management.change_alter_managment',login_url='/'),name="dispatch")
def edit_Alter_manager(request):#变更内容编辑用
    if request.user.has_perm('Alter_management.change_alter_managment'):
        form =EditAlterform(request.POST)
        if form.is_valid():
            id=form.cleaned_data.get("id")#变更ID
            AltType = form.cleaned_data.get("AltType")  # '关联类型'#
            AssociatedNumber =form.cleaned_data.get("AssociatedNumber")  # '关联编号'#
            Database = form.cleaned_data.get("Database")  # '数据库'#
            AlterContent =form.cleaned_data.get("AlterContent")  # 变更内容
            Alter_managment.objects.filter(id=id).update(altertypeid=AltType, associatedid=AssociatedNumber, databaseid=Database, altercontent=AlterContent, modifier=request.user.username
    ,modifytime=datetime.now(),reviewstatus='0')
            return resful.OK()
        else:
            return resful.params_error(message=form.get_error())
    else:
        return resful.unauth(message='您没有编辑的权限！')


# * @函数名: delete_Alter_manager
# * @功能描述: 删除变更内容
# * @作者: 郭军
# * @时间: 2019-6-30 15:28:19
# * @最后编辑时间: 2019-9-9 17:01:02
# * @最后编辑者: 郭军
@require_POST
@Alter_login_required
def delete_Alter_manager(request):#变更内容删除用
    if request.user.has_perm('Alter_management.change_alter_managment'):
        id=request.POST.get("id")
        try:
            Alter_managment.objects.filter(id=id).delete()
            return resful.OK()
        except:
            return resful.params_error(message="该变更不存在")
    else:
        return resful.unauth(message='您没有删除的权限！')



# * @函数名: add_Alter_managerView
# # * @功能描述: 添加变更内容
# # * @作者: 郭军
# # * @时间: 2019-6-30 15:28:19
# # * @最后编辑时间: 2019-9-3 10:00:36
# # * @最后编辑者: 郭军
class add_Alter_managerView(View):
    def get(self,request):

            Databases=Alt_Database.objects.all()
            context={
                'Databases':Databases
            }
            return render(request,'Alter_management/Alter.html',context=context)


    def post(self,request):#添加变更内容
        if request.user.has_perm('Alter_management.change_alter_managment'):
            form = Alterform(request.POST)
            #如果验证成功
            if form.is_valid():
                AltType_id=form.cleaned_data.get('AltType')
                AltTypes = Alt_Type.objects.get(pk=AltType_id)
                AssociatedNumber = form.cleaned_data.get('AssociatedNumber')
                Database_id = form.cleaned_data.get('Database')
                Database= Alt_Database.objects.get(pk=Database_id)
                AlterContent=form.cleaned_data.get('AlterContent')

                #判断变更内容在库中是否存在
                exists=Alter_managment.objects.filter(altercontent=AlterContent).exists()
                if not exists:
                    Alter_managment.objects.create(altertypeid=AltTypes.pk, associatedid=AssociatedNumber, databaseid=Database.pk,altercontent=AlterContent,
                                                   modifier=request.user.username)
                    return resful.OK()
                else:

                    return resful.params_error(message="该变更内容已经存在!")
            else:
                error = form.get_error()
                print(error)
                return resful.params_error(message=form.get_error())
        else:
            return resful.unauth(message='您没有添加变更的权限！')

# * @函数名: Review_Alter_manager
# * @功能描述: 变更审核
# * @作者: 郭军
# * @时间: 2019-6-30 09:39:03
# * @最后编辑时间: 2019-8-30 14:41:00
# * @最后编辑者: 郭军
@require_POST
@Alter_login_required
# @permission_required(perm= 'Alter_management.review_alter_managment',login_url='alter/Alter_manager/')
def Review_Alter_manager(request):#变更审核用
    if request.user.has_perm('Alter_management.review_alter_managment'):
        form =Reviewform(request.POST)
        if form.is_valid():
            id = form.cleaned_data.get('id')
            ReviewStatus = form.cleaned_data.get('ReviewStatus')  # '审核状态',
            ReviewContent = form.cleaned_data.get('ReviewContent')  # '审核内容',

            #更新主表审核状态
            Review=Alter_managment.objects.filter(id=id).update(reviewstatus=ReviewStatus, reviewcontent=ReviewContent, reviewer=request.user.username,reviewtime=datetime.now())

            #判断主表是否审核成功
            if Review:

                #取得主表数据
                alter_data = Alter_managment.objects.get(id=id)

                #获取分表数据
                alter_data_checked=Alter_managment_checked.objects.filter(alterid=id)

                #判断分表是否有满足条件的数据并且审核状态是未审核
                if alter_data_checked and ReviewStatus=='2':

                    #删除分表的数据
                    successdelete=alter_data_checked.delete()

                    if successdelete:
                        return resful.OK()
                    else:
                        return resful.params_error(message='分数据删除失败')

                else:
                    #如果审核通过则复制创建主表数据到分表
                    Alter_managment_checked.objects.create(alterid=alter_data.pk,associatedid=alter_data.associatedid,altercontent=alter_data.altercontent,modifier=alter_data.modifier,modifytime=alter_data.modifytime,reviewer=alter_data.reviewer,reviewstatus=alter_data.reviewstatus,reviewcontent=alter_data.reviewcontent,reviewtime=alter_data.reviewtime,altertypeid=alter_data.altertypeid,databaseid=alter_data.databaseid)
                    return resful.OK()
            else:
                return resful.params_error(message='审核失败！')
            return resful.OK()
        else:
           return resful.params_error(message=form.get_error())
    else:
        return resful.unauth(message='您没有审核的权限！')


# * @函数名: Alter_detail
# * @功能描述: 变更内容详情
# * @作者: 郭军
# * @时间: 2019-6-30 09:39:03
# * @最后编辑时间: 2019-8-30 14:41:00
# * @最后编辑者: 郭军
@Alter_login_required
def Alter_detail(request,id):#变更详情页面
        Alterdeatil =Alter_managment.objects.get(id=id)
        if Alterdeatil:
            context = {

                'Alterdeatil': Alterdeatil
            }
            return render(request,"Alter_management/Alter_detail.html",context=context)
        else:
            return resful.params_error(message='没有找到详情数据')


def test_review(request):
    id=request.GET.get('id')
    print('获取到的id是：',id)
    datas=Alter_managment.objects.values('pk','reviewstatus','reviewcontent').filter(pk=id)
    datas =list(datas)
    data ={'code':200,'data':datas}
    return JsonResponse(data,safe=False)
