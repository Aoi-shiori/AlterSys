#encoding:utf-8
#authenticate授权#
from django.contrib.auth import login,logout,authenticate
from  django.views.decorators.http import require_POST
from .froms import loginform
from  django.http import JsonResponse
from utils import resful
from django.shortcuts import render,redirect,reverse
from Apps.Alterauth.models import User
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