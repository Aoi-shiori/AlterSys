#encoding:utf-8
#authenticate授权#
from django.contrib.auth import login,logout,authenticate
from  django.views.decorators.http import require_POST
from .froms import loginform,AddStaffForm
from  django.http import JsonResponse
from utils import resful
from django.shortcuts import render,redirect,reverse
from Apps.Alterauth.models import User
from django.views.generic import View
from django.contrib.auth.models import Group



#只接收post请求
@require_POST
def login_view(request):
    form = loginform(request.POST)
    #如果验证成功
    if form.is_valid():
        MobilePhone = form.cleaned_data.get('MobilePhone')
        password = form.cleaned_data.get('password')
        remember = form.cleaned_data.get('remember')
        user = authenticate(request, username=MobilePhone, password=password)
        if user:
            if user.is_active:
                login(request,user)
                if remember:
                    #使用django默认的过期时间2周
                    request.session.set_expiry(None)
                else:
                    #如果没有记住我，浏览器关闭后自动过期
                    request.session.set_expiry(0)
                return resful.OK() and render(request, "Alter_management/index.html")
            else:
                return resful.unauth(message="您的账号未授权！")
        else:
            return resful.params_error(message="手机号码或者密码错误！")
    else:
        errors = form.get_error()
        return resful.servererror(message=errors)






def logout_view(request):
    logout(request)
    return redirect(reverse('management:login'))
    pass


#员工授权管理
def staff_view(request):
    #staffs=User.objects.all()
    staffs = User.object.all()
    context={
        'staffs':staffs
    }
    return  render(request,"Alter_management/staffs.html",context=context)

#添加员工
class AddStaff_view(View):
    def get(self,request):
        groups = Group.objects.all()
        context={
            'groups':groups
        }
        return render(request,'Alter_management/add_staff.html',context=context)

    def post(self,request):
        form =AddStaffForm(request.POST)
        if form.is_valid():
            MobilePhone=form.cleaned_data.get('MobilePhone')
            username = form.cleaned_data.get('username')
            password1 = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('MobilePhone')
            name =form.cleaned_data.get('name')
            Department =form.cleaned_data.get('Department')
            Permissions =form.cleaned_data.get('Permissions')
            #User.object.create_user(MobilePhone=MobilePhone, username=username, password=password1, email=email,
                                            #name=name, Department=Department, Permissions=Permissions)
            user=User.object.create_user(MobilePhone=MobilePhone,username=username,password=password1,email=email,name=name,Department=Department,Permissions=Permissions)
            groups_ids=form.cleaned_data.get('groups')
            groups= Group.objects.filter(pk__in=groups_ids)
            user.groups.set(groups)
            user.save()
            return resful.OK()
            #return redirect(reverse('Alterauth:add_staff'))
        else:
            return resful.params_error(message=form.get_error())
