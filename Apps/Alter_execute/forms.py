from django import forms
from Apps.forms import FormMixin

class Executeform(forms.Form,FormMixin):
        AlterID =forms.CharField(max_length=50)
        Hospital=forms.CharField(max_length=25)
        #Executor=forms.CharField(max_length=50)
        ExecutionResult=forms.CharField(widget=forms.Textarea)

class execute_ExecuteForm(forms.Form,FormMixin):
        executeID=forms.IntegerField(error_messages={"required":"必须传入执行id！"})
        AlterID =forms.CharField(max_length=50)
        Hospital=forms.CharField(max_length=25)
        #Executor=forms.CharField(max_length=50)
        ExecutionResult=forms.CharField(widget=forms.Textarea)