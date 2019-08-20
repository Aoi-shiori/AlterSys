from django.shortcuts import render

from django.views.generic import View
#导入只接受GET请求和POST请求的装饰器
from django.views.decorators.http import require_POST,require_GET
#导入form验证用的表单
from .forms import Executeform,execute_ExecuteForm
#导入Alter_execute的模型
from Apps.Alter_execute.models import Alter_execute
#导入变更数据模型
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

# 三、FileResponse对象
# class FileResponse(open_file,as_attachment=False,filename=",**kwargs)
#
# 如果as_attachment=True，则设置内容配置头，它要求浏览器将文件作为下载提供给用户。
# 如果open_file没有名称，或者open_file的名称不合适，则使用filename参数提供自定义文件名。
# FileResponse接受任何带有二进制内容的类文件对象。
# >>> from django.http import FileResponse
# >>> response = FileResponse(open('myfile.png', 'rb'))
from django.http import FileResponse

from Apps.Alter_Dict.models import DBname,AltType

#消息弹窗
from django.contrib import messages


#
from django.http import HttpResponse
#
import os
#
import glob

#
from django.http import StreamingHttpResponse




# 执行管理页面
class Alter_Execute_view(View):  # 变更执行管理页面，返回数据
    def get(self, request):
        # request.GET.get获取出来的数据都是字符串类型
        page = int(request.GET.get('p', 1))  # 获当前页数,并转换成整形，没有传默认为1
        start = request.GET.get('start')  # 获取时间控件开始时间
        end = request.GET.get('end')  # 获取时间控件结束时间
        cxtj = request.GET.get('cxtj')  # 获取查询条件录入信息
        # request.GET.get（参数,默认值）
        # 这个参数是只有没有传递参数的时候才会使用
        # 如果传递了，但是是一个空的字符串，也不会使用，那么可以使用 ('ReviewStatus',0) or 0
        reviewStatus = int(request.GET.get('ReviewStatus', 0))  # 获取审核状态查询值,因为get到的都是字符串，转换成整形才能在页面中用数值对比
        DatabaseType = int(request.GET.get('DatabaseType', 0))
        Databases = DBname.objects.all()
        Alterd_datas = Alter_managment.objects.filter(ReviewStatus='1')  # 获取所有数据库的数据

        if start or end:  # 查询时间判断
            if start:
                start_time = datetime.strptime(start, '%m/%d/%Y')
            else:
                start_time = datetime(year=2019, month=5, day=1)

            if end:
                end_time = datetime.strptime(end, '%m/%d/%Y')
            else:
                end_time = datetime.today()

            Alterd_datas = Alterd_datas.filter(ExecutionTime__range=(make_aware(start_time), make_aware(end_time)))

        if cxtj:  # 查询条件判断
            # 多条件模糊查询匹配，满足一个即可返回，用到Q对象格式如下
            Alterd_datas = Alterd_datas.filter(
                Q(id__icontains=cxtj) | Q(AlterID__icontains=cxtj) | Q(Hospital__icontains=cxtj) | Q(
                    Executor__icontains=cxtj) | Q(ExecutionResult__icontains=cxtj))

        if reviewStatus:  # 审核状态判断
            Alterd_datas = Alterd_datas.filter(ReviewStatus=reviewStatus)

        if DatabaseType:  # 数据库类型判断
            Alterd_datas = Alterd_datas.filter(Database=DatabaseType)

        paginator = Paginator(Alterd_datas, 2)  # 分页用，表示每2条数据分一页
        page_obj = paginator.page(page)  # 获取总页数

        context_date = self.get_pagination_data(paginator, page_obj)  # 调用分页函数获取到页码
        context = {
            'Alterd_datas': page_obj.object_list,
            'page_obj': page_obj,  # 将分了多少页的数据全部传过去
            'paginator': page,  # 当前页数据
            'start': start,
            'end': end,
            'cxtj': cxtj,
            'reviewStatus': reviewStatus,
            'DatabaseType': DatabaseType,
            'Databases': Databases,
            'url_query': '&' + parse.urlencode({
                'start': start or '',
                'end': end or '',
                'cxtj': cxtj or '',
                'reviewStatus': reviewStatus or '',
            })  # 用于拼接url,让页面在查询后进行翻页，任然保留查询条件

        }  # 返回包含分页信息的数据

        context.update(context_date)  # 将分页数据更新到context,返回返回给页面
        return render(request, "Alter_Execute/Alter_Execute.html", context=context)

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



#变更添加
@require_POST
def add_Alter_Execute(request):
    form = Executeform(request.POST)
    if form.is_valid():
        AlterID =form.cleaned_data.get('id')
        Hospital = form.cleaned_data.get('Hospital')
        #Executor = form.cleaned_data.get('Executor')
        ExecutionResult =form.cleaned_data.get('ExecutionResult')
        exists =Alter_execute.objects.filter(Hospital=Hospital).exists()
        if not exists:
            Alter_execute.objects.create(AlterID=AlterID,Hospital=Hospital,Executor=request.user.name,ExecutionResult=ExecutionResult)
            return resful.OK()
        else:
            return resful.params_error(message="该执行记录已经存在！")
    else:
        return resful.params_error(message=form.get_error())


def execute_Alter_Execute(request):
    form =execute_ExecuteForm(request.POST)
    if form.is_valid():
        id=form.cleaned_data.get('id')
        AlterID = form.cleaned_data.get('id')
        Hospital = form.cleaned_data.get('Hospital')
        ExecutionResult = form.cleaned_data.get('ExecutionResult')
        #获取字段的值
        # AlterIDnow=Alter_execute.objects.values('id').filter(executeID=executeID)
        # if int(id)>int(AlterIDnow):
        Alter_execute.objects.filter(id=id).update(AlterID=AlterID, Hospital=Hospital, Executor=request.user.name,ExecutionResult=ExecutionResult,ExecutionTime=datetime.now())
        return resful.OK()
    else:
        return resful.params_error(message="表单验证不通过！")


#删除变更执行数据
@require_POST
def delete_Alter_Execute(request):
    id =request.POST.get("id")
    try:
        Alter_execute.objects.filter(id=id).delete()
        return resful.OK()
    except:
        return resful.params_error(message="该变更执行数据不存在")


#export 变更内容导出
#
def export(request):
    #checked=request.POST.get('checked')
    checked =[1,2,3]
    #checked=[]


        #过滤出需要导出的数据
    exports =Alter_managment.objects.filter(pk__in=checked,ReviewStatus=0)


    if exports:
        #打开Alter.sql
        f = open(r'../AlterSys/Download/' + 'Alter.sql', "w", encoding='utf-8')
        #写入数据
        for export in exports:
            #写头部说明信息
            f.write('-- ----------------------------\n')
            f.write('-- ID:' + str(export.pk)+'\n-- 变更库:'+export.Database.Database+'\n')
            f.write('-- ----------------------------\n')
            ##判断是否以;结尾
            if export.AlterContent.endswith(';'):

                #，如果是以';'结尾,则进行换行操作
                f.write(export.AlterContent.replace(';',';\n'))

            else:
                # 如果不是';'结尾,添加';'结尾，并换行
                f.write(export.AlterContent+';'+'\n')

            #每个变更之间进行换行
            f.write('\n')

        f.close()

        #查找并打开文件
        file = open(r'../AlterSys/Download/'+'Alter.sql','rb')
        #赋予新的文件名 时间+_Alter.sql
        the_file_name = datetime.now().strftime('%Y%m%d%H%M%S')+'_Alter.sql'
        #FileResponse对象，接收二进制对象
        response =FileResponse(file)
        #设置返回二进制文件类型
        response['Content-Type'] = 'application/text/plain'
        #设置attachment，让浏览器下载，而不是直接打开，并重命名
        response['Content-Disposition'] = 'attachment;filename='+the_file_name
        return response
    else:
        return resful.params_error(message="需要导出的数据不存在")




#调用导出文件函数,测试用
#export()
