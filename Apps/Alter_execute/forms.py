from django import forms
from Apps.forms import FormMixin

class Executeform(forms.Form,FormMixin):
        AlterID =forms.CharField(max_length=50,error_messages={"required":'变更ID不能为空'})
        Hospital=forms.CharField(max_length=25,error_messages={"required":'医院不能为空'})
        #Executor=forms.CharField(max_length=50)
        ExecutionResult=forms.CharField(widget=forms.Textarea,error_messages={"required":'执行结果不能为空'})

class execute_ExecuteForm(forms.Form,FormMixin):
        executeID=forms.IntegerField(error_messages={"required":"必须传入执行id！"})
        AlterID =forms.CharField(max_length=50,error_messages={"required":'变更ID不能为空'})
        Hospital=forms.CharField(max_length=25,error_messages={"required":'医院不能为空'})
        #Executor=forms.CharField(max_length=50)
        ExecutionResult=forms.CharField(widget=forms.Textarea,error_messages={"required":'执行结果不能为空'})