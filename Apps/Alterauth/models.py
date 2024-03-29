#encoding:utf-8
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from shortuuidfield import ShortUUIDField
from django.db import models

class UserManager(BaseUserManager):
    def _create_user(self, mobilephone, worknumber, password, **kwargs):
        if not mobilephone:
            raise ValueError("请传入手机号码！")
        if not worknumber:
            raise ValueError('请传入用户名！')
        if not password:
            raise ValueError('请传入密码')
        user = self.model(mobilephone=mobilephone, worknumber=worknumber, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, mobilephone, worknumber, password, **kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(mobilephone, worknumber, password, **kwargs)

    def create_superuser(self, mobilephone, worknumber, password, **kwargs):
        kwargs['is_superuser'] = True
        kwargs['username'] = '超级管理员'
        #kwargs['worknumber'] = 'admin'
        return self._create_user(mobilephone, worknumber, password, **kwargs)



#用户表
class User(AbstractBaseUser,PermissionsMixin):
        #我们不是用默认的自增长的主键
        #ID会泄露注册用户数
        #因此我们是用UUID/shortuuid
        #所以需要一个第三方包，pip install django-shortuuidfield
        id = ShortUUIDField(primary_key=True) #用户唯一ID#
        # password = models.CharField(max_length=200)#密码#
        mobilephone = models.CharField(max_length=11, unique=True)#手机号码#
        email = models.EmailField(unique=True,null=True) #唯一的unique true#
        worknumber = models.CharField(max_length=100)#工号/用户名
        username = models.CharField(max_length=50)#姓名#
        department = models.CharField(max_length=100,null=True)#所在部门#
        #userpermissions = models.CharField(max_length=4)#用户权限0，管理员、1审核者，2提交者，3执行者#
        registrationtime = models.DateTimeField(auto_now_add=True)#注册时间#
        is_cancellation = models.BooleanField(default=False)#注销状态#
        USERNAME_FIELD = 'mobilephone'
        #telphone,username,password
        REQUIRED_FIELDS = ['worknumber']
        EMAIL_FIELD = 'email'


        object = UserManager()
        def get_full_name(self):
            return self.worknumber

        def get_short_name(self):
            return self.worknumber

        def get_user_name(self):
            return self.username

        class Meta:
            db_table = 'alt_user'



class ZtGroup(models.Model):
    name = models.CharField(max_length=30)
    role = models.CharField(max_length=30)
    desc = models.CharField(max_length=255)
    acl = models.TextField()

    class Meta:
        managed = False
        db_table = 'zt_group'


class ZtUser(models.Model):
    dept = models.PositiveIntegerField()
    account = models.CharField(unique=True, max_length=30)
    password = models.CharField(max_length=32)
    realname = models.CharField(max_length=100)
    role = models.CharField(max_length=10)
    nickname = models.CharField(max_length=60)
    commiter = models.CharField(max_length=100)
    avatar = models.CharField(max_length=30)
    birthday = models.DateField()
    gender = models.CharField(max_length=1)
    email = models.CharField(max_length=90)
    skype = models.CharField(max_length=90)
    qq = models.CharField(max_length=20)
    yahoo = models.CharField(max_length=90)
    gtalk = models.CharField(max_length=90)
    wangwang = models.CharField(max_length=90)
    mobile = models.CharField(max_length=11)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=120)
    zipcode = models.CharField(max_length=10)
    join = models.DateField()
    visits = models.PositiveIntegerField()
    ip = models.CharField(max_length=15)
    last = models.PositiveIntegerField()
    fails = models.IntegerField()
    locked = models.DateTimeField()
    ranzhi = models.CharField(max_length=30)
    score = models.IntegerField()
    scorelevel = models.IntegerField(db_column='scoreLevel')  # Field name made lowercase.
    deleted = models.CharField(max_length=1)
    status = models.CharField(max_length=7)

    class Meta:
        managed = False
        db_table = 'zt_user'




