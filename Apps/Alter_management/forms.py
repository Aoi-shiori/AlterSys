#encoding:utf-8
from django import forms
from Apps.forms import FormMixin
#表单数据验证

class Alterform(forms.Form,FormMixin):
        AlterType = forms.CharField(max_length=100)  # '关联类型'#
        AssociatedNumber = forms.CharField(max_length=50)  # '关联编号'#
        Datebase = forms.CharField(max_length=50)  # '数据库'#
        AlterContent = forms.CharField(widget=forms.Textarea)   # 变更内容
        Informant = forms.CharField(max_length=50)  # '填报人',

class EditAlterform(forms.Form):
        PriKey=forms.IntegerField(error_messages={"required":"必须传入AlterID!"})
        AlterType = forms.CharField(max_length=100)  # '关联类型'#
        AssociatedNumber = forms.CharField(max_length=50)  # '关联编号'#
        Datebase = forms.CharField(max_length=50)  # '数据库'#
        AlterContent = forms.CharField(widget=forms.Textarea)  # 变更内容
        Informant = forms.CharField(max_length=50)  # '填报人',
