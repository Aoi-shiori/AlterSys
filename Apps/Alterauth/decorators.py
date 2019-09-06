#encoding:utf-8
from utils import resful
from django.shortcuts import redirect
from functools import wraps
from django.http import Http404

def Alter_superuser_required(viewfunc):
    @wraps(viewfunc)
    def decorator(request,*args,**kwargs):
        if request.user.is_superuser:
            return viewfunc(request,*args,**kwargs)
        else:
            raise Http404()
    return decorator

def Alter_login_required(func):
    def wapper(request,*args,**kwargs):
            #如果用户是经过授权的
        if request.user.is_authenticated and request.user.is_cancellation==False:
            return func(request,*args,**kwargs)
        else:
            if request.is_ajax():
                return resful.unauth(message='请先登录')
            else:
                return redirect('management:login')
    return wapper