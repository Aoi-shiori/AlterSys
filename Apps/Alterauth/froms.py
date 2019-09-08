#encoding:utf-8
from django import forms
from Apps.forms import FormMixin
from .models import User
#表单数据验证

class loginform(forms.Form,FormMixin):
    MobilePhone = forms.CharField(max_length=11,min_length=11,error_messages={"max_length":"手机号码长度大于11位！","min_length":"密码最少不能少于11位！"})
    password = forms.CharField(max_length=16, min_length=6,error_messages={"max_length":"密码最多不能超过16个字符！","min_length":"密码最少不能少于6个字符！"})
    remember = forms.IntegerField(required=False)


class AddStaffForm(forms.Form,FormMixin):
    mobilephone = forms.CharField(max_length=11,min_length=11,error_messages={"required":"手机号码未填写","max_length":"手机号码不能大于11位！","min_length":"手机号码不能小于11位！"})
    worknumber = forms.CharField(max_length=100,error_messages={"required":"工号未填写"})  # 用户名#
    password1 = forms.CharField(max_length=16, min_length=6,error_messages={"required":"未填写密码","max_length":"密码最多不能超过16个字符！","min_length":"密码最少不能少于6个字符！"})
    password2 = forms.CharField(max_length=16, min_length=6,error_messages={"required":"未填写确认密码","max_length":"密码最多不能超过16个字符！","min_length":"密码最少不能少于6个字符！"})
    email = forms.EmailField(error_messages={"required":"邮箱地址未填写","invalid":'邮箱格式不正确'})
    username = forms.CharField(max_length=50,error_messages={"required":"姓名未填写"})  # 姓名#
    department = forms.CharField(max_length=100,error_messages={"required":"部门未填写"})  # 所在部门#
    groups=forms.CharField(error_messages={"required":"未勾选权限分组"})

    def clean(self):
        clean_Data = super(AddStaffForm,self).clean()
        password1 = clean_Data.get('password1')
        password2 = clean_Data.get('password2')
        mobilephone = clean_Data.get('mobilephone')
        worknumber = clean_Data.get('worknumber')
        email = clean_Data.get('email')

        if password1 != password2:
            raise forms.ValidationError('两次密码输入不一致！')
        #exists = User.object.filter(mobilephone=mobilephone).exists()
        if User.object.filter(mobilephone=mobilephone).exists():
            raise forms.ValidationError('该手机号码已经注册')
        if User.object.filter(worknumber=worknumber).exists():
            raise forms.ValidationError('该工号已注册')
        if User.object.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已经注册')
        return clean_Data

class EditStaffForm(forms.Form, FormMixin):
    id = forms.CharField(error_messages={"required":"必须传入uid！"})
    mobilephone = forms.CharField(max_length=11,error_messages={"required":"手机号码未填写","max_length":"手机号码不能大于11位！","min_length":"手机号码不能小于11位！"})
    worknumber = forms.CharField(max_length=100,error_messages={"required":"工号未填写"})  # 用户名#
    email = forms.EmailField(error_messages={"required":"邮箱地址未填写"})
    username = forms.CharField(max_length=50,error_messages={"required":"姓名未填写"})  # 姓名#
    department = forms.CharField(max_length=100,error_messages={"required":"部门未填写"})  # 所在部门#
    groups = forms.CharField(error_messages={"required":"未勾选权限分组"})

    def clean(self):
        clean_Data = super(EditStaffForm,self).clean()
        password1 = clean_Data.get('password1')
        password2 = clean_Data.get('password2')
        mobilephone = clean_Data.get('mobilephone')
        worknumber = clean_Data.get('worknumber')
        email = clean_Data.get('email')

        if password1 != password2:
            raise forms.ValidationError('两次密码输入不一致！')
        #exists = User.object.filter(mobilephone=mobilephone).exists()
        # if User.object.filter(mobilephone=mobilephone).exists():
        #     raise forms.ValidationError('该手机号码已经注册')
        # if User.object.filter(worknumber=worknumber).exists():
        #     raise forms.ValidationError('该工号已注册')
        # if User.object.filter(email=email).exists():
        #     raise forms.ValidationError('该邮箱已经注册')
        return clean_Data