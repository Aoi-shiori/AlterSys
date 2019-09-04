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
    MobilePhone = forms.CharField(max_length=11)
    username = forms.CharField(max_length=100)  # 用户名#
    password1 = forms.CharField(max_length=16, min_length=6,error_messages={"max_length":"密码最多不能超过16个字符！","min_length":"密码最少不能少于6个字符！"})
    password2 = forms.CharField(max_length=16, min_length=6,error_messages={"max_length":"密码最多不能超过16个字符！","min_length":"密码最少不能少于6个字符！"})
    email = forms.EmailField()
    name = forms.CharField(max_length=50)  # 姓名#
    Department = forms.CharField(max_length=100)  # 所在部门#
    Permissions = forms.CharField()# 审核权限
    groups=forms.CharField()

class EditStaffForm(forms.Form, FormMixin):
    id = forms.CharField(error_messages={"required":"必须传入uid！"})
    MobilePhone = forms.CharField(max_length=11)
    username = forms.CharField(max_length=100)  # 用户名#
    email = forms.EmailField()
    name = forms.CharField(max_length=50)  # 姓名#
    Department = forms.CharField(max_length=100)  # 所在部门#
    Permissions = forms.CharField()  # 审核权限
    groups = forms.CharField()

    # def clean(self):
    #     clean_Data = super(AddStaffForm,self).clean()
    #     password1 = clean_Data.get('password1')
    #     password2 = clean_Data.get('password2')
    #     if password1 != password2:
    #         raise forms.ValidationError('两次密码输入不一致！')
    #     exists = User.object.filter(MobilePhone=MobilePhone).exists()
    #     if exists:
    #         raise forms.ValidationError('该手机号码已经注册！')