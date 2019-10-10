#encoding:utf-8
#authenticate授权#
from django.contrib.auth import login,logout,authenticate
from  django.views.decorators.http import require_POST
from .froms import loginform,AddStaffForm,EditStaffForm
from  django.http import JsonResponse,HttpResponse
from utils import resful
from django.shortcuts import render,redirect,reverse
from Apps.Alterauth.models import User
from django.views.generic import View
from django.contrib.auth.models import Group
from Apps.Alterauth.decorators import Alter_login_required,Alter_superuser_required
from django.utils.decorators import method_decorator


#用户登录视图
#只接收post请求
@require_POST
def login_view(request):
    form = loginform(request.POST)
    #如果验证成功
    if form.is_valid():
        MobilePhone = form.cleaned_data.get('MobilePhone')
        Password = form.cleaned_data.get('password')
        remember = form.cleaned_data.get('remember')
        user = authenticate(request, mobilephone=MobilePhone, password=Password)
        if user:
            if user.is_active:
                login(request,user)
                if remember:
                    #使用django默认的过期时间2周
                    request.session.set_expiry(None)
                else:
                    #如果没有记住我，浏览器关闭后自动过期
                    request.session.set_expiry(0)
                # return resful.OK() and render(request, "Alter_management/index.html")
                return resful.OK()
            else:
                return resful.unauth(message="您的账号已经被注销了！")
        else:
            return resful.params_error(message="手机号码或者密码错误！")
    else:
        errors = form.get_error()
        return resful.servererror(message=errors)






def logout_view(request):
    logout(request)
    return redirect(reverse('management:login'))
    pass


#员工授权管理,加了装饰器，未授权则跳转登陆页面
@Alter_login_required
def staff_view(request):
    #staffs=User.objects.all()
    staffs = User.object.all()
    context={
        'staffs':staffs
    }
    return  render(request,"Alter_management/staffs.html",context=context)



# * @函数名: AddStaff_view
# # * @功能描述: 添加员工
# # * @作者: 郭军
# # * @时间: 2019-6-30 15:28:19
# # * @最后编辑时间: 2019-9-10 11:13:11
# # * @最后编辑者: 郭军
#添加员工,类视图需要借助其他工具才能使用装饰器,导入method_decorator
@method_decorator(Alter_superuser_required,name='dispatch')
class AddStaff_view(View):
    def get(self,request):
        groups = Group.objects.all()
        context={
            'groups':groups
        }
        return render(request,'Alter_management/add_staff.html',context=context)

    def post(self,request):
        if request.user.has_perm('Alterauth.change_user'):
            form =AddStaffForm(request.POST)
            if form.is_valid():
                mobilephone=form.cleaned_data.get('mobilephone')
                worknumber = form.cleaned_data.get('worknumber')
                password1 = form.cleaned_data.get('password1')
                email = form.cleaned_data.get('email')
                username =form.cleaned_data.get('username')
                department =form.cleaned_data.get('department')

                user=User.object.create_user(mobilephone=mobilephone,worknumber=worknumber,password=password1,email=email,username=username,department=department)
                #groups_ids=request.POST.getlist('groups')
                #groups= Group.objects.filter(pk__in=groups_ids)
                groups = form.cleaned_data.get('groups').split(',')
                #gs = groups.split(',')
                groups = Group.objects.filter(pk__in=groups)
                user.groups.set(groups)
                user.save()
                return resful.OK()
                #return redirect(reverse('Alterauth:add_staff'))
            else:
                return resful.params_error(message=form.get_error())
        else:
            return resful.unauth(message='您没有添加员工的权限！')


# * @函数名: EditStaff_view
# # * @功能描述: 编辑员工
# # * @作者: 郭军
# # * @时间: 2019-6-30 15:28:19
# # * @最后编辑时间: 2019-9-10 11:13:43
# # * @最后编辑者: 郭军
# @method_decorator(Alter_superuser_required,name='dispatch')
class EditStaff_view(View):
    def get(self,request):
        id =request.GET.get('id')
        Userdata = User.object.get(id=id)
        Groups_use = Userdata.groups.all()
        groups = Group.objects.all()
        context={
            'Use':Userdata,
            'Groups':Groups_use,
            'groups':groups,
        }
        return render(request,'Alter_management/add_staff.html',context=context)

    def post(self,request):
        if request.user.has_perm('Alterauth.change_user'):
            form =EditStaffForm(request.POST)
            if form.is_valid():
                id = form.cleaned_data.get('id')
                mobilephone=form.cleaned_data.get('mobilephone')
                worknumber = form.cleaned_data.get('worknumber')
                email = form.cleaned_data.get('email')
                username =form.cleaned_data.get('username')
                department =form.cleaned_data.get('department')

                exists = User.object.filter(id=id).exists()
                if exists:
                    users = User.object.exclude(id=id)
                    if  users.filter(mobilephone=mobilephone):
                        return resful.params_error(message='该手机号码已经注册，请重新输入！')
                    elif users.filter(worknumber=worknumber):
                        return resful.params_error(message='该工号已经注册，请重新输入！')
                    elif users.filter(email=email):
                        return resful.params_error(message='该邮箱地址已经注册，请重新输入！')
                    else:
                        User.object.filter(id=id).update(mobilephone=mobilephone,worknumber=worknumber,email=email,username=username,department=department)
                        use=User.object.get(id=id) #获取到当前的用户，如果直接使用上面的是一个值

                        if User.object.get(id=id).is_superuser:
                            use.save()
                            #return resful.OK()
                            return resful.OK()
                        else:
                            groups = form.cleaned_data.get('groups').split(',')
                            #gs = groups.split(',')#将获取的字符串列表进行分割
                            group = Group.objects.filter(pk__in=groups)
                            use.groups.clear() #清除原有的分组权限数据
                            use.groups.set(group)
                            use.save()
                            return resful.OK()
                #return redirect(reverse('Alterauth:add_staff'))
            else:
                return resful.params_error(message=form.get_error())
        else:
            return resful.unauth(message='您没有编辑用户的权限！')



# * @函数名: Cancellation
# # * @功能描述: 注销启用员工
# # * @作者: 郭军
# # * @时间: 2019-6-30 15:28:19
# # * @最后编辑时间: 2019-9-10 11:14:16
# # * @最后编辑者: 郭军
@method_decorator(Alter_superuser_required,name='dispatch')
def Cancellation(request):
    if request.user.has_perm('Alterauth.change_user'):
        id=request.POST.get('id').replace(',','') #传过来的uid后面带了个逗号，进行去除
        Cancellation=request.POST.get('Cancellation')
        if Cancellation == 'True':
            User.object.filter(id=id).update(Cancellation=False)
            return resful.OK()
        else:
            User.object.filter(id=id).update(Cancellation=True)
            return resful.OK()
    else:
        return resful.unauth(message='您没有注销员工的权限！')