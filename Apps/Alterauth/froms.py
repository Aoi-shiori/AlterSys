#encoding:utf-8
from django import forms
from Apps.forms import FormMixin
#表单数据验证

class loginform(forms.Form,FormMixin):
    MobilePhone = forms.CharField(max_length=11)
    password = forms.CharField(max_length=16, min_length=6,error_messages={"max_length":"密码最多不能超过16个字符！","min_length":"密码最少不能少于6个字符！"})
    remember = forms.IntegerField(required=False)
