#encoding:utf-8
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from  shortuuidfield import ShortUUIDField
from django.db import models

class  UsermManager(BaseUserManager):
    def _create_user(self,mobilephone,username ,password, **kwargs):
        if not mobilephone:
            raise ValueError("请传入手机号码！")
        if not username:
            raise ValueError('请传入用户名！')
        if not password:
            raise ValueError('请传入密码')
        user = self.model(mobilephone=mobilephone, username=username, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, mobilephone, username, password, **kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(mobilephone, username, password, **kwargs)

    def create_superuser(self, mobilephone, username, password, **kwargs):
        kwargs['is_superuser'] = True
        return self._create_user(mobilephone, username, password, **kwargs)




class User(AbstractBaseUser,PermissionsMixin):
        #我们不是用默认的自增长的主键
        #ID会泄露注册用户数
        #因此我们是用UUID/shortuuid
        #所以需要一个第三方包，pip install django-shortuuidfield
        uid = ShortUUIDField(primary_key=True) #用户唯一ID#
        email = models.EmailField(unique=True) #唯一的unique true#
        password = models.CharField(max_length=200)#密码#
        MobilePhone = models.CharField(max_length=11,unique=True)#手机号码#
        username = models.CharField(max_length=100)#用户名#
        name = models.CharField(max_length=50)#姓名#
        Department = models.CharField(max_length=100)#所在部门#
        Permissions = models.CharField(max_length=2)#用户权限#
        RegistrationTime = models.DateTimeField(auto_now_add=True)#注册时间#
        Cancellation = models.BooleanField(default=True)#是否有效#

        USERNAME_FIELD = 'MobilePhone'
        #telphone,username,password
        REQUIRED_FIELDS = ['username']
        EMAIL_FIELD = 'emil'

        object = UsermManager()
        def get_full_name(self):
            return self.username

        def get_short_name(self):
            return self.username

