import json
from django.core import serializers
from django.shortcuts import render

from django.views.generic import View
#导入只接受GET请求和POST请求的装饰器
from django.views.decorators.http import require_POST,require_GET
#导入form验证用的表单
from .forms import Executeform,execute_ExecuteForm
#导入Alter_execute的模型
from Apps.Alter_execute.models import Alter_execute
#导入变更数据模型
from Apps.Alter_management.models import Alter_managment,Alter_managment_checked
#导出医院字典模型
from Apps.Alter_Dict.models import Alt_Hospital

#导入我们重构的resful文件，用于返回结果代码和消息，详细可以看resful.py文件
from utils import resful
#导入分页用的类
from django.core.paginator import Paginator
#导入时间分类
from datetime import datetime
#导入设置时区
import pytz
#将时间标记为清醒的时间
from django.utils.timezone import make_aware
#用于模糊查询
from django.db.models import Q
#用于拼接url
from urllib import parse

from django.http import JsonResponse

# 三、FileResponse对象
# class FileResponse(open_file,as_attachment=False,filename=",**kwargs)
#
# 如果as_attachment=True，则设置内容配置头，它要求浏览器将文件作为下载提供给用户。
# 如果open_file没有名称，或者open_file的名称不合适，则使用filename参数提供自定义文件名。
# FileResponse接受任何带有二进制内容的类文件对象。
# >>> from django.http import FileResponse
# >>> response = FileResponse(open('myfile.png', 'rb'))
from django.http import FileResponse

from Apps.Alter_Dict.models import Alt_Database,Alt_Hospital

from django.views.decorators.csrf import csrf_exempt



# * @函数名: Alter_Execute_view
# * @功能描述: 执行管理页面数据展示视图
# * @作者: 郭军
# * @时间: 2019-06-22 10:01:00
# * @最后编辑时间: 2019-8-30 15:25:30
# * @最后编辑者: 郭军
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

        # 获取数据库类型查询值,因为get到的都是字符串，转换成整形才能在页面中用数值对比
        DatabaseType = int(request.GET.get('DatabaseType', 0))

        #过滤数据库类型数据
        Databases = Alt_Database.objects.all()

        # 过滤医院类型数据
        Hospital = Alt_Hospital.objects.all()

        # 获取所有数据库的数据
        Alterd_datas = Alter_managment_checked.objects.all()  # 获取所有数据库的数据


        if start or end:  # 查询时间判断
            if start:
                start_time = datetime.strptime(start, '%m/%d/%Y')
            else:
                start_time = datetime(year=2019, month=5, day=1)

            if end:
                end_time = datetime.strptime(end, '%m/%d/%Y')
            else:
                end_time = datetime.today()

            Alterd_datas = Alterd_datas.filter(modifytime__range=(make_aware(start_time), make_aware(end_time)))

        if cxtj:  # 查询条件判断
            # 多条件模糊查询匹配，满足一个即可返回，用到Q对象格式如下
            Alterd_datas = Alterd_datas.filter(Q(alterid=cxtj)|Q(altercontent__icontains=cxtj)|Q(modifier__icontains=cxtj)|Q(associatednumber__icontains=cxtj))


        if DatabaseType:  # 数据库类型判断
            Alterd_datas = Alterd_datas.filter(databaseid=DatabaseType)



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
            'DatabaseType': DatabaseType,
            'Databases': Databases,
            'Hospital':Hospital,
            'url_query': '&' + parse.urlencode({
                'start': start or '',
                'end': end or '',
                'cxtj': cxtj or '',
                'DatabaseType': DatabaseType,
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


# * @函数名: alter_execute_history_view
# * @功能描述: 变更数据导出执行历史记录视图
# * @作者: 郭军
# * @时间: 2019-8-30 15:28:19
# * @最后编辑时间: 22019-8-30 15:28:27
# * @最后编辑者: 郭军
class alter_execute_history_view(View):  # 变更执行管理页面，返回数据
    def get(self, request):
        # request.GET.get获取出来的数据都是字符串类型
        page = int(request.GET.get('p', 1))  # 获当前页数,并转换成整形，没有传默认为1
        start = request.GET.get('start')  # 获取时间控件开始时间
        end = request.GET.get('end')  # 获取时间控件结束时间
        cxtj = request.GET.get('cxtj')  # 获取查询条件录入信息
        # request.GET.get（参数,默认值）
        # 这个参数是只有没有传递参数的时候才会使用
        # 如果传递了，但是是一个空的字符串，也不会使用，那么可以使用 ('ReviewStatus',0) or 0
        Hospital = int(request.GET.get('Hospital', 0))  # 获取医院ID,因为get到的都是字符串，转换成整形才能在页面中用数值对比

        # 获取执行记录库所有的数据
        Alterd_datas = Alter_execute.objects.all()

        #
        Hospital_datas = Alt_Hospital.objects.all()

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
                Q(id__icontains=cxtj) | Q(AlterID__icontains=cxtj) | Q(
                    Executor__icontains=cxtj) | Q(ExecutionResult__icontains=cxtj))

        if Hospital:  # 审核状态判断
            Alterd_datas = Alterd_datas.filter(Hospital_id=Hospital)


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
            'Hospital_datas':Hospital_datas,
            'url_query': '&' + parse.urlencode({
                'start': start or '',
                'end': end or '',
                'cxtj': cxtj or '',
                'Hospital': Hospital or '',
            })  # 用于拼接url,让页面在查询后进行翻页，任然保留查询条件

        }  # 返回包含分页信息的数据

        context.update(context_date)  # 将分页数据更新到context,返回返回给页面
        return render(request, "Alter_Execute/Alter_execute_history.html", context=context)

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



# * @函数名: export
# * @功能描述: 导出当前条件下所有变更内容
# * @作者: 郭军
# * @时间: 2019-08-22 10:01:00
# * @最后编辑时间: 2019-8-23 15:22:19
# * @最后编辑者: 郭军
@csrf_exempt
def export(request):
    #checked=request.POST.get('checked')
    #checked =[1,2,3]
    #checked=[]
    Database =request.POST.get('DatabaseType')
    Hospital = request.POST.get('Hospital')

    #过滤出需要导出的数据
    #exports =Alter_managment.objects.filter(pk__in=checked,ReviewStatus=1)
    #Database =1




    if Database != '0':
        exports = Alter_managment.objects.filter(ReviewStatus=1,Database=Database)
    else:
        exports = Alter_managment.objects.filter(ReviewStatus=1)



    # 获取当前导出数据的ID列表
    Exports_Nums = list(exports.values_list('id', flat=True))
    # 将列表转换成字符串，用于存储数据库
    Exports_Nums = ','.join([str(id) for id in Exports_Nums])
    print('转换字符串', Exports_Nums)


    if exports:

        ids = exports.values_list('id')
        nowMax = list(max(ids))[0]
        #打开Alter.sql
        f = open(r'../AlterSys/Download/' + 'Alter.sql', "w", encoding='utf-8')
        #写入数据
        for export in exports:
            #写头部说明信息
            f.write('-- ----------------------------\n')
            f.write('-- ID:' + str(export.pk)+'\n-- 变更库:'+export.Database.Database+'\n')
            f.write('--审核时间：'+str(export.AuditTime.strftime("%Y-%m-%d %H:%M:%S"))+'\n')
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
        #response['Content-Type'] = 'application/text/plain'
        response['Content-Type'] = 'application/octet/stream'
        #设置attachment，让浏览器下载，而不是直接打开，并重命名
        response['Content-Disposition'] = 'attachment;filename='+the_file_name


        #判断当前用户，在执行表中是否有记录
        exits=Alter_execute.objects.filter(UID=request.user.id)



        if exits:
            #存在-更新数据
            #AA=exits.values_list('AlterID')
            #BB=exits.values('AlterID')
            #CC=list(AA)[0][0]
            #hh=CC[0]
            #DD=BB.get('AlterID')
            AlterID = exits.values_list('alterid')
            OldID=list(AlterID)[0][0]



            #判断还是有点问题 需要修改一下
            if nowMax < int(OldID):
                exits.update(AlterID=OldID,Executor=request.user.username,ExecutionTime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),ExecutionResult='本次执行到变更ID：'+str(nowMax),UID=request.user.id,Exports=Exports_Nums)

            else:
                exits.update(AlterID=nowMax,Executor=request.user.username,ExecutionTime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),ExecutionResult='本次执行到变更ID：'+str(nowMax),UID=request.user.id,Exports=Exports_Nums)

        else:
            #不存在-插入数据
            Alter_execute.objects.create(AlterID=nowMax,Hospital=Hospital,Executor=request.user.username,ExecutionTime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),ExecutionResult='首次执行到变更ID：'+str(nowMax),UID=request.user.id,Exports=Exports_Nums)

        return resful.OK()
    else:
        return resful.params_error(message="需要导出的数据不存在")


# * @函数名: export_New
# * @功能描述: 导出最新的变更内容
# * @作者: 郭军
# * @时间: 2019-08-23 15:01:00
# * @最后编辑时间: 2019-8-23 15:22:19
# * @最后编辑者: 郭军
@csrf_exempt
def export_New(request):
    #获取被选中的
    #checked=request.POST.get('checked')
    #获取当前选中的数据库类型
    Database =request.POST.get('DatabaseType')
    Hospital =request.POST.get('Hospital')

    print('医院ID是',Hospital)
    #过滤数据库中可导出数据
    Export_News_datas=Alter_managment.objects.filter(ReviewStatus=1)

    if Export_News_datas:
        # 过滤出需要导出的数据
        # exports =Alter_managment.objects.filter(pk__in=checked,ReviewStatus=1)

        # 获取可导出数据中，ID最大的值
        Now_MaxNum = max(Export_News_datas.values_list('id', flat=True))

        # 获取当前导出数据的ID列表
        Exports_Nums = list(Export_News_datas.values_list('id', flat=True))

        #判断导出执行表中是否有导出的记录
        Alt_execute=Alter_execute.objects.filter(UID=request.user.pk)
        if Alt_execute:
            # 获取用户已导出的数据
            Export_old_Nums = Alt_execute.objects.values_list('exportlist', flat=True)[0]

            # 字符串转换成数值列表
            Export_old_Nums = [int(id) for id in (Export_old_Nums.split(','))]

            # 获取不在已导出列中的ID
            # export_meiyou = [x for x in Exports_Nums if  x not in Export_old_Nums]
            # print('还没有导出的ID有', export_meiyou)

            # 过滤出还未导出的数据
            Export_News_datas = Export_News_datas.exclude(pk__in=Export_old_Nums)
        else:
            pass
        # 判断数据库类型是否选中
        if Database != '0':
            # 当选择的不是全部，根据数据库类型过滤出数据
            Export_News_datas = Export_News_datas.filter(Database=Database)
        else:
            Export_News_datas

        if Export_News_datas:

            # 列表转换成字符串
            # Exports_Nums=','.join([str(id) for id in Exports_Nums])
            # print('转换字符串',Exports_Nums)

            # 字符串转换成列表
            # Exports_Nums=[int(id) for id in (Exports_Nums.split(','))]
            #
            # print('转换列表',Exports_Nums)

            # 打开Alter.sql
            f = open(r'../AlterSys/Download/' + 'Alter.sql', "w", encoding='utf-8')
            # 写入数据
            for export_News_data in Export_News_datas:
                # 写头部说明信息
                f.write('-- ----------------------------\n')
                f.write('-- ID:' + str(export_News_data.pk) + '\n-- 变更库:' + export_News_data.Database.Database + '\n')
                f.write('--审核时间：' + str(export_News_data.AuditTime.strftime("%Y-%m-%d %H:%M:%S")) + '\n')
                f.write('-- ----------------------------\n')
                ##判断是否以;结尾
                if export_News_data.AlterContent.endswith(';'):

                    # ，如果是以';'结尾,则进行换行操作
                    f.write(export_News_data.AlterContent.replace(';', ';\n'))

                else:
                    # 如果不是';'结尾,添加';'结尾，并换行
                    f.write(export_News_data.AlterContent + ';' + '\n')

                # 每个变更之间进行换行
                f.write('\n')

            f.close()

            # 查找并打开文件
            file = open(r'../AlterSys/Download/' + 'Alter.sql', 'rb')
            # 赋予新的文件名 时间+_Alter.sql
            the_file_name = datetime.now().strftime('%Y%m%d%H%M%S') + '_Alter.sql'
            # FileResponse对象，接收二进制对象
            response = FileResponse(file)
            # 设置返回二进制文件类型
            # response['Content-Type'] = 'application/text/plain'
            response['Content-Type'] = 'application/octet/stream'
            # 设置attachment，让浏览器下载，而不是直接打开，并重命名
            response['Content-Disposition'] = 'attachment;filename=' + the_file_name

            # 判断当前用户，在执行表中是否有记录
            exits = Alter_execute.objects.filter(UID=request.user.id)

            if exits:
                # 存在-更新数据
                # AA=exits.values_list('AlterID')
                # BB=exits.values('AlterID')
                # CC=list(AA)[0][0]
                # hh=CC[0]
                # DD=BB.get('AlterID')

                # 获取已经导出的最大ID
                Old_AlterID = list(exits.values_list('alterid'))[0][0]

                # 将列表转换成字符串，用于存储数据库
                Exports_Nums = ','.join([str(id) for id in Exports_Nums])
                print('转换字符串', Exports_Nums)

                # 判断还是有点问题 需要修改一下
                if Now_MaxNum < int(Old_AlterID):
                    exits.update(AlterID=Old_AlterID, Hospital_id=Hospital, Executor=request.user.username,
                                 ExecutionTime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                 ExecutionResult='本次执行到变更ID：' + str(Now_MaxNum), UID=request.user.id)

                else:
                    exits.update(AlterID=Now_MaxNum, Hospital_id=Hospital, Executor=request.user.username,
                                 ExecutionTime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                 ExecutionResult='本次执行到变更ID：' + str(Now_MaxNum), UID=request.user.id,
                                 Exports=Exports_Nums)

            else:
                # 不存在-插入数据
                Alter_execute.objects.create(AlterID=Now_MaxNum, Hospital_id=Hospital, Executor=request.user.username,
                                             ExecutionTime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                             ExecutionResult='首次执行到变更ID：' + str(Now_MaxNum), UID=request.user.id,
                                             Exports=Exports_Nums)

            return resful.OK()
        else:
            return resful.params_error(message="需要导出的数据不存在")
    else:
     return  resful.params_error(message='没有可导出的数据！')




# * @函数名: export_alt_datas
# * @功能描述: 生成导出变更数据
# * @作者: 郭军
# * @时间: 2019-8-30 09:39:03
# * @最后编辑时间: 2019-8-30 14:41:00
# * @最后编辑者: 郭军
# @csrf_exempt
def export_alt_data(request):
    print(request.COOKIES.values())

    #获取当前选中的数据库类型
    databaseId =request.POST.get('database')
    # databaseId =1

    #获取当前选择的医院ID
    hospitalId =request.POST.get('hospital')
    # hospitalId =1

    #调试用：打印获取到的数据
    print('获取到的数据库ID是:',databaseId)
    print('获取到的医院ID是:',hospitalId)

    if hospitalId != '0':
        # 过滤出可导出数据
        exportData = Alter_managment_checked.objects.filter(reviewstatus=1)

        # 过滤数据库类型
        if databaseId != '0':
            # 当选择的不是全部，根据数据库类型过滤出数据
            exportData = exportData.filter(dbnumber_id=databaseId)
        else:
            exportData

        # 判断是否有可导出数据
        if exportData:

            # 获取可导出数据中，ID最大的值
            export_max_alter_id = max(exportData.values_list('id', flat=True))

            # 获取当前导出数据的ID列表
            exportNumbers = list(exportData.values_list('id', flat=True))

            # 将列表转换成字符串，用于存储数据库
            exportNumbers = ','.join([str(id) for id in exportNumbers])
            print('转换字符串', exportNumbers)

            # 导出执行表中是否有历史导出记录
            exportHistoryData = Alter_execute.objects.filter(userid=request.user.pk, hospital_id=hospitalId)

            if exportHistoryData:

                # 获取用户已导出的数据
                Export_old_Nums = exportHistoryData.values_list('exportlist', flat=True)[0]

                # 获取已经导出的最大ID
                old_alter_id = list(exportHistoryData.values_list('alterid'))[0][0]

                # 字符串转换成数值列表
                Export_old_Nums = [int(id) for id in (Export_old_Nums.split(','))]

                # 过滤出还未导出的数据
                # exportData = exportData.exclude(pk__in=Export_old_Nums)


                if exportData:
                    # 调用导出文件生成函数
                    File_Generate = Export_file_Generate(exportData)
                else:
                    return resful.params_error(message='您已经导出过数据至最新！')


                if File_Generate:

                    # 判断当前导出的最大ID否比原来的小
                    if export_max_alter_id < int(old_alter_id):

                        exportHistoryData.update(Executor=request.user.username,
                                                 ExecutionTime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                 ExecutionResult='本次执行到变更ID：' + str(export_max_alter_id),
                                                 UID=request.user.id)

                    else:

                        exportHistoryData.update(AlterID=export_max_alter_id, Executor=request.user.username,
                                                 ExecutionTime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                 ExecutionResult='本次执行到变更ID：' + str(export_max_alter_id),
                                                 UID=request.user.id,
                                                 Exports=exportNumbers)
                    return resful.OK()
                else:
                    return resful.params_error(message='导出文件生成失败！')
            else:

                File_Generate = Export_file_Generate(exportData)

                if File_Generate:
                    # 创建新的导出执行记录
                    Alter_execute.objects.create(AlterID=export_max_alter_id, Hospital_id=int(hospitalId),
                                                 Executor=request.user.username,
                                                 ExecutionTime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                 ExecutionResult='首次执行到变更ID：' + str(export_max_alter_id),
                                                 UID=request.user.id,
                                                 Exports=exportNumbers)
                    return resful.OK()
                else:
                    return resful.params_error(message='导出文件生成失败！')

        else:
            return resful.params_error(message='当前条件无可导出数据！')

    else:
        return resful.params_error(message='请选择医院！')







# * @函数名: download
# * @功能描述: 获取导出的Sql文件重命名后返回文件进行下载
# * @作者: 郭军
# * @时间: 2019-08-22 16:01:00
# * @最后编辑时间: 2019-8-23 15:26:38
# * @最后编辑者: 郭军
# @csrf_exempt
def download(request):
        # 查找并打开文件
        file = open(r'../AlterSys/Download/' + 'Alter.sql', 'rb')
        # 赋予新的文件名 时间+_Alter.sql
        the_file_name = datetime.now().strftime('%Y%m%d%H%M%S') + '_Alter.sql'
        # FileResponse对象，接收二进制对象
        response = FileResponse(file)
        # 设置返回二进制文件类型
        # response['Content-Type'] = 'application/text/plain'
        response['Content-Type'] = 'application/octet/stream'
        # 设置attachment，让浏览器下载，而不是直接打开，并重命名
        response['Content-Disposition'] = 'attachment;filename=' + the_file_name

        print('用户下载文件' + the_file_name)
        return response
        # return resful.ajax_ok(message="",data=response)



# * @函数名: Export_file_Generate
# * @功能描述: 生成导出文件
# * @作者: 郭军
# * @时间: 2019-8-30 09:34:30
# * @最后编辑时间: 2019-8-30 09:34:37
# * @最后编辑者: 郭军
def Export_file_Generate(export_datas):
    if export_datas:
            # 打开Alter.sql
            f = open(r'../AlterSys/Download/' + 'Alter.sql', "w", encoding='utf-8')
            # 写入数据
            for export_data in export_datas:
                # 写头部说明信息
                f.write('-- ----------------------------\n')
                f.write('-- 变更ID:' + str(export_data.alterid) + '\n-- 变更库:' + str(export_data.databaseid) + '\n')
                f.write('--审核时间：' + str(export_data.reviewtime.strftime("%Y-%m-%d %H:%M:%S")) + '\n')
                f.write('-- ----------------------------\n')
                ##判断是否以;结尾
                if export_data.altercontent.endswith(';'):

                    # ，如果是以';'结尾,则进行换行操作
                    f.write(export_data.altercontent.replace(';', ';\n'))

                else:
                    # 如果不是';'结尾,添加';'结尾，并换行
                    f.write(export_data.altercontent + ';' + '\n')

                # 每个变更之间进行换行
                f.write('\n')

            f.close()
            return True
    else:
        return False


def test_select(request):
    #取到需要的元组
    hospitaldict=Alt_Hospital.objects.all().values("pk", "hospitalname")
    #转换列表
    hospitaldict=list(hospitaldict)
    # 取到需要的元组
    databasedict = Alt_Database.objects.all().values("pk", "dbname")
    # 转换列表
    databasedict=list(databasedict)

    #组合成新的字典
    datas={'code':200,'database':databasedict,'hospital':hospitaldict}
    # data = serializers.serialize("json",hospitalData)
    # return resful.ajax_ok(message="",data=list(datas))

    # return  JsonResponse(list(datas),safe=False) #返回json数据对象，safe=false:允许将非字典转换json
    return  JsonResponse(datas,safe=False) #返回json数据对象，safe=false:允许将非字典转换json
    # return  JsonResponse({'status':200,'msg':'ok','data':list(hospitalData)})



# * @函数名: export_alt_datas_view
# * @功能描述: 1、get请求：返回医院字典、数据库字典的json数据 2、post请求：根据请求生成导出变更数据并生成。
# * @作者: 郭军
# * @时间: 2019-9-5 16:12:55
# * @最后编辑时间: 2019-9-5 16:20:00
# * @最后编辑者: 郭军
# @csrf_exempt
class export_alt_datas_view(View):
    #get请求：返回医院字典、数据库字典的json数据
    def get(self,request):
        # 取到需要的元组
        hospitaldict = Alt_Hospital.objects.all().values("pk", "hospitalname")
        # 转换列表
        hospitaldict = list(hospitaldict)
        # 取到需要的元组
        databasedict = Alt_Database.objects.all().values("pk", "dbname")
        # 转换列表
        databasedict = list(databasedict)

        # 组合成新的字典
        datas = {'code': 200, 'database': databasedict, 'hospital': hospitaldict}
        # data = serializers.serialize("json",hospitalData)
        # return resful.ajax_ok(message="",data=list(datas))

        # return  JsonResponse(list(datas),safe=False) #返回json数据对象，safe=false:允许将非字典转换json
        return JsonResponse(datas, safe=False)  # 返回json数据对象，safe=false:允许将非字典转换json
        # return  JsonResponse({'status':200,'msg':'ok','data':list(hospitalData)})

    #根据请求生成导出变更数据并生成
    def post(self,request):
        print(request.COOKIES.values())

        # 获取当前选中的数据库类型
        databaseId = request.POST.get('database')
        # databaseId =1

        # 获取当前选择的医院ID
        hospitalId = request.POST.get('hospital')
        # hospitalId =1

        # 调试用：打印获取到的数据
        print('获取到的数据库ID是:', databaseId)
        print('获取到的医院ID是:', hospitalId)

        if hospitalId != '0'and databaseId != '0':
            # 过滤出可导出数据
            exportData = Alter_managment_checked.objects.filter(reviewstatus=1,databaseid=databaseId)

            # # 过滤数据库类型
            # if databaseId != '0':
            #     # 当选择的不是全部，根据数据库类型过滤出数据
            #     exportData = exportData.filter(databaseid=databaseId)
            # else:
            #     exportData

            # 判断是否有可导出数据
            if exportData:

                # 获取可导出数据中，ID最大的值
                    #方法一：数据转换成列表，并且指定返回指定字段的值列表(flat=True),不加设置返回的是字典
                export_max_alter_ids = max(exportData.values_list('id', flat=True))
                    #方法二：将数据按指定字典id 从大到小进行排序，然后取首条数据的id值，这里是主键也就可以用Pk
                export_max_alter_id =exportData.order_by('-id').first().pk


                # 获取当前导出数据的ID列表
                exportNumbers = list(exportData.values_list('id', flat=True))

                # 将列表转换成字符串，用于存储数据库
                exportNumbers = ','.join([str(id) for id in exportNumbers])
                print('转换字符串', exportNumbers)

                # 导出执行表中是否有历史导出记录
                exportHistoryData = Alter_execute.objects.filter(userid=request.user.pk, hospitalid=int(hospitalId),databaseid=databaseId)



                if exportHistoryData:

                    # # 获取用户已导出的数据
                    # Export_old_Nums = exportHistoryData.values_list('exportlist', flat=True)[0]

                    # 获取已经导出的最大ID
                    #old_alter_id = list(exportHistoryData.values_list('alterid'))[0][0] #切片的方式获取id
                    old_alter_id = Alter_execute.objects.get(userid=request.user.pk, hospitalid=int(hospitalId), databaseid=databaseId).alterid

                    # # 字符串转换成数值列表
                    # Export_old_Nums = [int(id) for id in (Export_old_Nums.split(','))]

                    # # 过滤出还未导出的数据,将不在已导出列表中的数据过滤出来
                    # exportData = exportData.exclude(pk__in=Export_old_Nums)

                    #过滤出ID大于当前alterid的数据
                    exportData=exportData.filter(id__gt=old_alter_id)

                    if exportData:
                        # 调用导出文件生成函数
                        File_Generate = Export_file_Generate(exportData)
                    else:
                        return resful.params_error(message='您已经导出过数据至最新！')

                    if File_Generate:

                        # 判断当前导出的最大ID否比原来的小
                        if export_max_alter_id < int(old_alter_id):

                            exportHistoryData.update(executor=request.user.username,
                                                     executiontime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                     executionresult='本次执行到ID：' + str(export_max_alter_id),
                                                     userid=request.user.id)

                        else:

                            exportHistoryData.update(alterid=export_max_alter_id, executor=request.user.username,
                                                     executiontime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                     executionresult='本次执行到ID：' + str(export_max_alter_id),
                                                     userid=request.user.id,
                                                     exportlist=exportNumbers)
                        return resful.OK()
                    else:
                        return resful.params_error(message='导出文件生成失败！')
                else:

                    File_Generate = Export_file_Generate(exportData)

                    if File_Generate:
                        # 创建新的导出执行记录
                        Alter_execute.objects.create(alterid=export_max_alter_id, hospitalid=int(hospitalId),
                                                     executor=request.user.username,databaseid=databaseId,
                                                     executiontime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                     executionresult='首次执行到变更ID：' + str(export_max_alter_id),
                                                     userid=request.user.id,
                                                     exportlist=exportNumbers)
                        return resful.OK()
                    else:
                        return resful.params_error(message='导出文件生成失败！')

            else:
                return resful.params_error(message='当前条件无可导出数据！')

        else:
            return resful.params_error(message='必须选择医院和数据库！')


