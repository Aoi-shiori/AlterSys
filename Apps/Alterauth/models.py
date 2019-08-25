#encoding:utf-8
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from shortuuidfield import ShortUUIDField
from django.db import models

class UserManager(BaseUserManager):
    def _create_user(self, MobilePhone, Username, password, **kwargs):
        if not MobilePhone:
            raise ValueError("请传入手机号码！")
        if not Username:
            raise ValueError('请传入用户名！')
        if not password:
            raise ValueError('请传入密码')
        user = self.model(MobilePhone=MobilePhone, Username=Username,**kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, MobilePhone, Username, Email, password, **kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(MobilePhone, Username, Email, password, **kwargs)

    def create_superuser(self, MobilePhone, Username, password, **kwargs):
        kwargs['is_superuser'] = True
        kwargs['Permissions'] = True
        return self._create_user(MobilePhone, Username, password, **kwargs)



#用户表
class User(AbstractBaseUser,PermissionsMixin):
        #我们不是用默认的自增长的主键
        #ID会泄露注册用户数
        #因此我们是用UUID/shortuuid
        #所以需要一个第三方包，pip install django-shortuuidfield
        id = ShortUUIDField(primary_key=True) #用户唯一ID#
        Email = models.EmailField(unique=True) #唯一的unique true#
        # password = models.CharField(max_length=200)#密码#
        MobilePhone = models.CharField(max_length=11,unique=True)#手机号码#
        Username = models.CharField(max_length=100)#用户名#
        Name = models.CharField(max_length=50)#姓名#
        Department = models.CharField(max_length=100)#所在部门#
        Permissions = models.BooleanField(default=False)#用户权限0，管理员、1审核者，2提交者，3执行者#
        RegistrationTime = models.DateTimeField(auto_now_add=True)#注册时间#
        Cancellation = models.BooleanField(default=False)#注销状态#
        USERNAME_FIELD = 'MobilePhone'
        #telphone,username,password
        REQUIRED_FIELDS = ['Username']
        EMAIL_FIELD = 'Email'


        object = UserManager()
        def get_full_name(self):
            return self.Username

        def get_short_name(self):
            return self.Username

        class Meta:
            db_table = 'alt_user'
