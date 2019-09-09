from django import forms
from Apps.forms import FormMixin


class DB_Dict_Form(forms.Form,FormMixin):
    pk=forms.IntegerField(error_messages={'required':'必须传入分类ID！'})
    Database = forms.CharField(max_length=100,error_messages={'required':"数据库类型名称不能为空！",'max_length':'超出字段最大值，请重新填写','empty_value':'名称不能为空！'})
class DB_Dict_addForm(forms.Form,FormMixin):
    Database = forms.CharField(max_length=100,error_messages={'required':"数据库类型名称不能为空！",'max_length':'超出字段最大值，请重新填写','empty_value':'名称不能为空！'})

class AltType_Dict_Form(forms.Form,FormMixin):
    pk =forms.IntegerField(error_messages={'required':"必须传入分类ID！"})
    altertypename=forms.CharField(max_length='100',error_messages={'required':"变更类型名称不能为空！",'max_length':'超出字段最大值，请重新填写','empty_value':'名称不能为空！'})

class AltType_Dict_addForm(forms.Form,FormMixin):
    AltType=forms.CharField(max_length='100',error_messages={'required':"变更类型名称不能为空！",'max_length':'超出字段最大值，请重新填写','empty_value':'名称不能为空！'})

class Hospital_Dict_Form(forms.Form,FormMixin):
    pk =forms.IntegerField(error_messages={'required':"必须传入分类ID！"})
    Hospital=forms.CharField(max_length='100',error_messages={'required':"医院名称不能为空！",'max_length':'超出字段最大值，请重新填写','empty_value':'名称不能为空！'})

class Hospital_Dict_addForm(forms.Form,FormMixin):
    hospital=forms.CharField(max_length='100',error_messages={'required':"医院名称不能为空！",'max_length':'超出字段最大值，请重新填写','empty_value':'名称不能为空！'})