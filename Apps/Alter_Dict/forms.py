from django import forms
from Apps.forms import FormMixin


class DB_Dict_Form(forms.Form,FormMixin):
    pk=forms.IntegerField(error_messages={'required':'必须传入分类ID！'})
    Database = forms.CharField(max_length=100,error_messages={'required':"数据库类型不能为空！"})

class AltType_Dict_Form(forms.Form,FormMixin):
    pk =forms.IntegerField(error_messages={'required':"必须传入分类ID！"})
    AltType=forms.CharField(max_length='100',error_messages={'required':"变更类型不能为空！"})