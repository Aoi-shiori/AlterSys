#encoding:utf-8
from django import forms
from Apps.forms import FormMixin
from Apps.Alter_management.models import Alter_managment
#表单数据验证

class Alterform(forms.Form,FormMixin):
        AlterType = forms.CharField(max_length=100)  # '关联类型'#
        AssociatedNumber = forms.CharField(max_length=50)  # '关联编号'#
        Datebase = forms.CharField(max_length=50)  # '数据库'#
        #如果数据库中字段是textfield时，
        AlterContent = forms.CharField(widget=forms.Textarea)  # 变更内容
        Informant = forms.CharField(max_length=50)  # '填报人',
        class Meta:
                model=Alter_managment
                exclude={'AlterType','AssociatedNumber','Datebase','AlterContent','Informant'}


class EditAlterform(forms.Form,FormMixin):
        AlterID=forms.IntegerField(error_messages={"required":"必须传入变更id！"})
        AlterType = forms.CharField(max_length=100)  # '关联类型'#
        AssociatedNumber = forms.CharField(max_length=50)  # '关联编号'#
        Datebase = forms.CharField(max_length=50)  # '数据库'#
        AlterContent = forms.CharField(widget=forms.Textarea)  # 变更内容
        Informant = forms.CharField(max_length=50)  # '填报人',
        # class Meta:
        #         model=Alter_managment
        #         exclude={'AlterType','AssociatedNumber','Datebase','AlterContent','Informant'}
