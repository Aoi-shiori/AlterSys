import json
from django.core import serializers
from django.shortcuts import render,HttpResponse

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
from datetime import datetime,timedelta
#导入设置时区
import pytz
#将时间标记为清醒的时间
from django.utils.timezone import make_aware,timezone
#用于模糊查询
from django.db.models import Q,F
#用于拼接url
from urllib import parse

from django.http import JsonResponse
import os
import zipfile37

from django.utils.encoding import escape_uri_path

# 三、FileResponse对象
# class FileResponse(open_file,as_attachment=False,filename=",**kwargs)
#
# 如果as_attachment=True，则设置内容配置头，它要求浏览器将文件作为下载提供给用户。
# 如果open_file没有名称，或者open_file的名称不合适，则使用filename参数提供自定义文件名。
# FileResponse接受任何带有二进制内容的类文件对象。
# >>> from django.http import FileResponse
# >>> response = FileResponse(open('myfile.png', 'rb'))
from django.http import FileResponse

from Apps.Alter_Dict.models import Alt_Database,Alt_Hospital,Alt_Type,CtDepartment

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

        #
        Altertype = Alt_Type.objects.all()

        # 过滤医院类型数据
        Hospital = Alt_Hospital.objects.all()

        # 获取所有数据库的数据
        Alterd_datas = Alter_managment_checked.objects.all()  # 获取所有数据库的数据

        if start or end:  # 查询时间判断
            if start:
                start_time = datetime.strptime(start, "%Y/%m/%d")
            else:
                start_time = datetime.today()-timedelta()

            if end:
                end_time = datetime.strptime(end, "%Y/%m/%d")+timedelta(hours=23,minutes=59,seconds=59)
            else:
                end_time = datetime.today()

            #Alterd_datas = Alterd_datas.filter(modifytime__range=(make_aware(start_time), make_aware(end_time)))
            Alterd_datas = Alterd_datas.filter(modifytime__range=(start_time, end_time))

        if cxtj:  # 查询条件判断
            # 多条件模糊查询匹配，满足一个即可返回，用到Q对象格式如下
            Alterd_datas = Alterd_datas.filter(Q(alterid=cxtj)|Q(altercontent__icontains=cxtj)|Q(modifier__icontains=cxtj)|Q(associatedid__icontains=cxtj))


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
            'AltTypes':Altertype,
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
        # current_page为当前页码数，count_page为每页显示数量
        # strat = (current_page - 1) * count_page
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
            'start_num':start_num
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

        # 过滤医院类型数据
        # Hospitals = Alt_Hospital.objects.all()
        Hospitals = CtDepartment.objects.using('ct_department').all()

        #过滤数据库类型数据
        Databases = Alt_Database.objects.all()

        #过滤出变更类型数据
        Altertypes = Alt_Type.objects.all()


        if start or end:  # 查询时间判断
            if start:
                start_time = datetime.strptime(start, '%Y/%m/%d')
            else:
                start_time = datetime(year=2019, month=5, day=1)

            if end:
                #end_time = datetime.strptime(end, '%Y/%m/%d')
                end_time = datetime.strptime(end, '%Y/%m/%d')+timedelta(hours=23,minutes=59,seconds=59)
            else:
                end_time = datetime.today()

            #Alterd_datas = Alterd_datas.filter(executiontime__range=(make_aware(start_time), make_aware(end_time)))
            Alterd_datas = Alterd_datas.filter(executiontime__range=(start_time, end_time))

        if cxtj:  # 查询条件判断
            # 多条件模糊查询匹配，满足一个即可返回，用到Q对象格式如下
            Alterd_datas = Alterd_datas.filter(
                Q(id=cxtj) | Q(alterid=cxtj) | Q(
                    executor__icontains=cxtj) | Q(executionresult__contains=cxtj))

        if Hospital:  # 审核状态判断
            Alterd_datas = Alterd_datas.filter(hospitalid=Hospital)


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
            'Hospitals':Hospitals,
            'Databases':Databases,
            'Altertypes':Altertypes,
            'url_query': '&' + parse.urlencode({
                'start': start or '',
                'end': end or '',
                'cxtj': cxtj or '',
                'Hospital': Hospital or '0',
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
        # current_page为当前页码数，count_page为每页显示数量
        #strat = (current_page - 1) * count_page
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
            'start_num':start_num
        }


# * @函数名: download
# * @功能描述: 获取导出的Sql文件重命名后返回文件进行下载
# * @作者: 郭军
# * @时间: 2019-08-22 16:01:00
# * @最后编辑时间: 2019-8-23 15:26:38
# * @最后编辑者: 郭军
@csrf_exempt
def download(request):
        dbname =request.GET.get('dbname')
        print('獲取到的數據庫名稱是：',dbname)
        hospitalid = request.GET.get('hospitalid')
        print('獲取到的醫院編號是：', hospitalid)
        databaseid = request.GET.get('databaseid')
        print('獲取到的数据库編號是：', databaseid)


        # 查找并打开文件
        # file = open(r'../AlterSys/Download/' + 'Alter.sql', 'rb')
        file = open(r'../AlterSys/Download/' + databaseid+'.sql', 'rb')
        # 赋予新的文件名 时间+_Alter.sql
        # the_file_name = ('%s''%s'+datetime.now().strftime('%Y%m%d%H%M%S') +'_alter.sql')%(hospitalid,dbname)
        the_file_name = hospitalid+'_'+dbname+'_'+datetime.now().strftime('%Y%m%d%H%M%S') +'.sql'
        # the_file_name =hospitalid+datetime.now().strftime('%Y%m%d%H%M%S') + '數據庫_alter.sql'
        # the_file_name =hospitalid+ '數據庫_alter.sql'
        print('生成的文件名是：', the_file_name)

        # FileResponse对象，接收二进制对象
        response = FileResponse(file)
        # 设置返回二进制文件类型
        # response['Content-Type'] = 'application/text/plain'
        response['Content-Type'] = 'application/octet/stream'
        # 设置attachment，让浏览器下载，而不是直接打开，并重命名
        # response['Content-Disposition'] = 'attachment;filename=' +the_file_name
        # response['Content-Disposition'] = 'attachment;filename='.format(the_file_name)
        response['Content-Disposition'] = 'attachment;filename='+the_file_name.encode('utf-8').decode('ISO-8859-1')
        # response['Content-Disposition'] = 'attachment;filename='+the_file_name+''
        # response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
        # response['Content-Disposition'] = 'attachment;filename*=utf-8''{}'.format(the_file_name)

        print('用户下载文件:' + the_file_name)
        return response
        # return resful.ajax_ok(message="",data=response)



# * @函数名: Export_file_Generate
# * @功能描述: 生成导出文件
# * @作者: 郭军
# * @时间: 2019-8-30 09:34:30
# * @最后编辑时间: 2019-8-30 09:34:37
# * @最后编辑者: 郭军
def Export_file_Generate(request,export_datas,hospitalId,databaseid):
    if export_datas:
            #将数据按照修改时间从小到大排序，如果要倒序则加负号'-'
            export_datas.order_by('modifytime') #从小到大排序
            # export_datas.order_by('-modifytime')


            # 打开Alter.sql
            f = open(r'../AlterSys/Download/' + str(databaseid)+'.sql', "w", encoding='utf-8')

            # 写入数据
            for export_data in export_datas:
                # 写头部说明信息
                f.write('-- ----------------------------\n')
                # f.write('-- 变更ID:' + str(export_data.alterid) +'\n-- 执行医院:' + str(Alt_Hospital.objects.get(pk=hospitalId).hospitalname) + '\n-- 变更库:' + str(Alt_Database.objects.get(pk=export_data.databaseid).dbname) + '\n')
                f.write('-- 变更ID:' + str(export_data.alterid) +'\n-- 执行医院:' + str(CtDepartment.objects.using('ct_department').get(pk=hospitalId,dept_id=F('branchcode')).dept_name) + '\n-- 变更库:' + str(Alt_Database.objects.get(pk=export_data.databaseid).dbname) + '\n')
                f.write('-- 修改时间:' + str(export_data.modifytime.strftime("%Y-%m-%d %H:%M:%S")) + '\n')
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
                f.write('-- ----------------------------\n')
                f.write('-- 执行记录表-执行记录插入\n')
                f.write('-- ----------------------------\n')
                #id,userid,alterid,hospitalid,databaseid,executor,executiontime,executionresult,exportlist

                alterid =export_datas.order_by('-alterid').values().first()['alterid']
                # databaseid =export_datas.values().first()['databaseid']
                executor = request.user.username
                userid=request.user.pk
                T1 =datetime.now()
                T2 =datetime.utcnow()
                executiontime = datetime.now().astimezone(pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S")
                #两种在字符串中引用变量的方法
            f.write('''INSERT INTO `alt_execute` VALUES (NULL, '{0}', '{1}', {2}, {3}, '{4}', '{5}', '执行到变更ID：{6}', '2');\n'''.format(userid,alterid,hospitalId,databaseid,executor,executiontime,alterid))
            f.write('''INSERT INTO `alt_execute` VALUES (NULL, '%s', '%s', %s, %s, '%s', '%s', '行到变更ID：%s', '2');\n'''%(userid,alterid,hospitalId,databaseid,executor,executiontime,alterid))
            f.write('''INSERT INTO `alt_execute` VALUES (NULL, '%s', '%s', %s, %s, '%s', '%s', '执行到变更ID：%s', '2');\n'''%(userid,alterid,hospitalId,databaseid,executor,executiontime,alterid))

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
        #hospitaldict = Alt_Hospital.objects.all().values("pk", "hospitalname")
        # hospitaldict = CtDepartment.objects.using('ct_department').all().values("dept_id", "dept_name")
        hospitaldict = CtDepartment.objects.using('ct_department').filter(branchcode=F('dept_id'))
        hospitaldict = hospitaldict.values("dept_id", "dept_name")
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


            #获取当前请求医院创建时间
            # begintime=Alt_Hospital.objects.get(pk=hospitalId).begintime
            begintime=CtDepartment.objects.using('ct_department').get(pk=hospitalId,branchcode=hospitalId).modified_date

            # 过滤出提交时间在医院创建时间后的数据
            exportData = exportData.filter(modifytime__gt=begintime)

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
                #export_max_alter_ids = max(exportData.values_list('id', flat=True))
                    #方法二：将数据按指定字典id 从大到小进行排序，然后取首条数据的id值，这里是主键也就可以用Pk
                export_max_alter_id =exportData.order_by('-id').first().pk


                # 获取当前导出数据的ID列表
                exportNumbers = list(exportData.values_list('id', flat=True))

                # 将列表转换成字符串，用于存储数据库
                exportNumbers = ','.join([str(id) for id in exportNumbers])
                print('转换字符串', exportNumbers)

                # 导出执行表中是否有历史导出记录
                exportHistoryData = Alter_execute.objects.filter(userid=request.user.pk, hospitalid=hospitalId,databaseid=databaseId)



                if exportHistoryData:

                    # # 获取用户已导出的数据
                    # Export_old_Nums = exportHistoryData.values_list('exportlist', flat=True)[0]

                    # 获取已经导出的最大ID
                    #old_alter_id = list(exportHistoryData.values_list('alterid'))[0][0] #切片的方式获取id
                    old_alter_id = Alter_execute.objects.get(userid=request.user.pk, hospitalid=hospitalId, databaseid=databaseId).alterid

                    # # 字符串转换成数值列表
                    # Export_old_Nums = [int(id) for id in (Export_old_Nums.split(','))]

                    # # 过滤出还未导出的数据,将不在已导出列表中的数据过滤出来
                    # exportData = exportData.exclude(pk__in=Export_old_Nums)

                    #过滤出ID大于当前alterid的数据
                    exportData=exportData.filter(id__gt=old_alter_id)

                    if exportData:

                        # 调用导出文件生成函数
                        File_Generate = Export_file_Generate(request,exportData,hospitalId)
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

                    File_Generate = Export_file_Generate(request,exportData,hospitalId,databaseId)

                    if File_Generate:
                        # 创建新的导出执行记录
                        Alter_execute.objects.create(alterid=export_max_alter_id, hospitalid=hospitalId,
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
        #↓↓↓↓↓如果选择了全部数据库↓↓↓↓↓↓↓
        elif hospitalId!='0' and databaseId =='0':
            database=Alt_Database.objects.all().order_by('id')
            dblist = []
            for db in database:

                # 过滤出可导出数据
                exportData = Alter_managment_checked.objects.filter(reviewstatus=1, databaseid=db.pk)

                # 获取当前请求医院创建时间
                # begintime=Alt_Hospital.objects.get(pk=hospitalId).begintime
                # begintime = CtDepartment.objects.using('ct_department').get(pk=hospitalId).modified_date

                # 过滤出提交时间在医院创建时间后的数据
                # exportData = exportData.filter(modifytime__gt=begintime)

                # # 过滤数据库类型
                # if databaseId != '0':
                #     # 当选择的不是全部，根据数据库类型过滤出数据
                #     exportData = exportData.filter(databaseid=databaseId)
                # else:
                #     exportData

                # 判断是否有可导出数据
                if exportData:


                    # 获取可导出数据中，ID最大的值
                    # 方法一：数据转换成列表，并且指定返回指定字段的值列表(flat=True),不加设置返回的是字典
                    # export_max_alter_ids = max(exportData.values_list('id', flat=True))
                    # 方法二：将数据按指定字典id 从大到小进行排序，然后取首条数据的id值，这里是主键也就可以用Pk
                    export_max_alter_id = exportData.order_by('-id').first().pk

                    # 获取当前导出数据的ID列表
                    exportNumbers = list(exportData.values_list('id', flat=True))

                    # 将列表转换成字符串，用于存储数据库
                    exportNumbers = ','.join([str(id) for id in exportNumbers])
                    print('转换字符串', exportNumbers)

                    # 导出执行表中是否有历史导出记录
                    exportHistoryData = Alter_execute.objects.filter(userid=request.user.pk, hospitalid=hospitalId,
                                                                     databaseid=db.pk)

                    if exportHistoryData:

                        # # 获取用户已导出的数据
                        # Export_old_Nums = exportHistoryData.values_list('exportlist', flat=True)[0]

                        # 获取已经导出的最大ID
                        # old_alter_id = list(exportHistoryData.values_list('alterid'))[0][0] #切片的方式获取id
                        old_alter_id = Alter_execute.objects.get(userid=request.user.pk, hospitalid=hospitalId,
                                                                 databaseid=db.pk).alterid

                        # # 字符串转换成数值列表
                        # Export_old_Nums = [int(id) for id in (Export_old_Nums.split(','))]

                        # # 过滤出还未导出的数据,将不在已导出列表中的数据过滤出来
                        # exportData = exportData.exclude(pk__in=Export_old_Nums)

                        # 过滤出ID大于当前alterid的数据
                        exportData = exportData.filter(id__gt=old_alter_id)

                        if exportData:

                            # 记录生成文件的数据库id
                            dblist.append(db.pk)

                            # 调用导出文件生成函数
                            File_Generate = Export_file_Generate(request, exportData, hospitalId, db.pk)
                        else:
                            continue
                            # return resful.params_error(message='您已经导出过数据至最新！')

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
                            # return resful.OK()
                        else:
                            return resful.params_error(message='导出文件生成失败！')
                    else:

                        File_Generate = Export_file_Generate(request, exportData, hospitalId,db.pk)

                        if File_Generate:

                            #记录生成文件的数据库id
                            dblist.append(db.pk)

                            # 创建新的导出执行记录
                            Alter_execute.objects.create(alterid=export_max_alter_id, hospitalid=hospitalId,
                                                         executor=request.user.username, databaseid=db.pk,
                                                         executiontime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                         executionresult='首次执行到变更ID：' + str(export_max_alter_id),
                                                         userid=request.user.id,
                                                         exportlist=exportNumbers)
                            # return resful.OK()
                        else:
                            return resful.params_error(message='导出文件生成失败！')
                else:
                    pass
                    # return resful.params_error(message='当前条件无可导出数据！')
            print('有数据的数据库列表是：',dblist)
            # return resful.OK()
            if dblist:

                return resful.ajax_ok(data=dblist)
            else:
                return resful.params_error(message='无可下载文件或已经下载至最新！')
        else:
            return resful.params_error(message='必须选择医院！')



# * @函数名: new_file_down
# * @功能描述: 1、新的文件下载函数。
# * @作者: 郭军
# * @时间: 2019-9-18 15:14:56
# * @最后编辑时间: 2019-9-18 15:15:01
# * @最后编辑者: 郭军
@csrf_exempt
def new_file_down(request):
    """
    下载压缩文件
    :param request:
    :param id: 数据库id
    :return:
    """
    # data = [{"id": "1", "image": "animation.jpg"}]  # 模拟mysql表数据
    # file_name = ""  # 文件名
    # for i in data:
    #     if i["id"] == id:  # 判断id一致时
    #         file_name = i["image"]  # 覆盖变量
    hospitalid =request.GET.get('hospitalid')
    dblist =request.GET.get('dblist')
    dblist=[k for k in (dblist.split(','))]
    print('已生产文件的数据库列表是：',dblist)
    dbnamelist = Alt_Database.objects.all().order_by('id')
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    file_path1 = os.path.join(base_dir, 'Download')  # 保存zip文件的路径
    zippath = os.path.join(file_path1, 'Alterzip')
    zip = zipfile37.ZipFile(zippath, 'w')

    for db in dblist:
            #获取数据库名称
            dbname = Alt_Database.objects.get(pk=int(db)).dbname

            #用来查找根据数据库id命名生成的sql文件
            file_name=db+'.sql'

            #用于重命名写入压缩包中的文件名
            file_names =str(hospitalid)+'_'+dbname+'_数据库' +'.sql'

            # base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 项目根目录

            base_dir=os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))#找到项目根目录
            # base_dir1=os.path.abspath(os.path.dirname(os.getcwd()))
            # base_dir2=os.path.abspath(os.path.join(os.getcwd(), ".."))
            # base_dir3=os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            # base_dir4=os.path.abspath(os.path.dirname(__file__))
            # file_path = os.path.join(base_dir, 'upload', 'images', file_name)  # 下载文件的绝对路径
            file_path = os.path.join(base_dir, 'Download', file_name)  # 下载文件的绝对路径

            # if not os.path.isfile(file_path):  # 判断下载文件是否存在
            #     # return HttpResponse("Sorry but Not Found the File")
            #     return resful.params_error(message=("未找到%s文件！")%(file_name))

            #在内存中将文件写入压缩包，并重命名
            zip.write(file_path,file_names)
    #将内存中的文件写入到硬盘中
    zip.close()



    def file_iterator(file_path, chunk_size=512):
        """
        文件生成器,防止文件过大，导致内存溢出
        :param file_path: 文件绝对路径
        :param chunk_size: 块大小
        :return: 生成器
        """
        with open(file_path, mode='rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    try:
        #压缩包文件名
        # zip_file_name = Alt_Hospital.objects.get(pk=hospitalid).hospitalname+'_'+str(hospitalid)+'_数据库变更压缩包'
        zip_file_name = CtDepartment.objects.using('ct_department').get(dept_id=hospitalid,branchcode=F('dept_id')).dept_name+'_'+str(hospitalid)+'_数据库变更压缩包'

        file_path = os.path.join(base_dir, 'Download', 'Alterzip')
        print('压缩文件地址是：',file_path)

        # 设置响应头
        # StreamingHttpResponse将文件内容进行流式传输，数据量大可以用这个方法
        response = FileResponse(file_iterator(file_path))
        # 以流的形式下载文件,这样可以实现任意格式的文件下载
        response['Content-Type'] = 'application/octet-stream'
        # Content-Disposition就是当用户想把请求所得的内容存为一个文件的时候提供一个默认的文件名
        # response['Content-Disposition'] = 'attachment;filename="{}.zip"'.format(file_name).encode('utf-8').decode('ISO-8859-1')
        #压缩包文件重新命名
        response['Content-Disposition'] = 'attachment;filename="{}.zip"'.format(zip_file_name).encode('utf-8').decode('ISO-8859-1')
    except:
        # return HttpResponse("Sorry but Not Found the File")
        # return resful.params_error(message="未找到文件！")
        return HttpResponse("未找到文件或从数据库中获取文件名失败！")
    print(zip_file_name+'.zip文件下载成功!')
    return response



def test(request):
    export_datas=Alter_managment_checked.objects.all()
    hospitalId ='1111'
    success=test_file_Generate(request,export_datas,hospitalId)
    if success:
        return HttpResponse('文件生成成功')
    else:
        return HttpResponse('文件生成失败!')


# * @函数名: test_file_Generate
# * @功能描述: 测试生成导出文件
# * @作者: 郭军
# * @时间: 2019-9-18 15:35:02
# * @最后编辑时间: 2019-9-18 15:35:09
# * @最后编辑者: 郭军
def test_file_Generate(request,export_datas,hospitalId):
    if export_datas:
            #将数据按照修改时间从小到大排序，如果要倒序则加负号‘-
            export_datas.order_by('modifytime') #从小到大排序
            # export_datas.order_by('-modifytime')
            # 打开Alter.sql
            dbnamelist = Alt_Database.objects.all()
            for db in dbnamelist:
                filename= db.dbname
                # f = open(r'../AlterSys/Download/' + 'Alter.sql', "w", encoding='utf-8')
                f = open(r'../AlterSys/Download/' + filename+'.sql', "w", encoding='utf-8')
                    # 写入数据
                for export_data in export_datas:
                        # 写头部说明信息
                        f.write('-- ----------------------------\n')
                        # f.write('-- 变更ID:' + str(export_data.alterid) +'\n-- 执行医院:' + str(Alt_Hospital.objects.get(pk=hospitalId).hospitalname) + '\n-- 变更库:' + str(Alt_Database.objects.get(pk=export_data.databaseid).dbname) + '\n')
                        # f.write('-- 变更ID:' + str(export_data.alterid) +'\n-- 执行医院:' + str(CtDepartment.objects.using('ct_department').get(pk=hospitalId).dept_name) + '\n-- 变更库:' + str(Alt_Database.objects.get(pk=export_data.databaseid).dbname) + '\n')
                        # f.write('-- 提交时间:' + str(export_data.modifytime.strftime("%Y-%m-%d %H:%M:%S")) + '\n')
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
                        f.write('-- ----------------------------\n')
                        f.write('-- 执行记录表-执行记录插入\n')
                        f.write('-- ----------------------------\n')
                        #id,userid,alterid,hospitalid,databaseid,executor,executiontime,executionresult,exportlist

                        alterid =export_datas.order_by('-alterid').values().first()['alterid']
                        databaseid =export_datas.values().first()['databaseid']
                        executor = request.user.username
                        userid=request.user.pk
                        T1 =datetime.now()
                        T2 =datetime.utcnow()
                        executiontime = datetime.now().astimezone(pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S")
                        #两种在字符串中引用变量的方法
                f.write('''INSERT INTO `alt_execute` VALUES (NULL, '{0}', '{1}', {2}, {3}, '{4}', '{5}', '执行到变更ID：{6}', '2');\n'''.format(userid,alterid,hospitalId,databaseid,executor,executiontime,alterid))
                f.write('''INSERT INTO `alt_execute` VALUES (NULL, '%s', '%s', %s, %d, '%s', '%s', '行到变更ID：%s', '2');\n'''%(userid,alterid,hospitalId,databaseid,executor,executiontime,alterid))
                f.write('''INSERT INTO `alt_execute` VALUES (NULL, '%s', '%s', %s, %s, '%s', '%s', '执行到变更ID：%s', '2');\n'''%(userid,alterid,hospitalId,databaseid,executor,executiontime,alterid))

                f.close()
            return True
    else:
        return False


