from django import forms
from Apps.forms import FormMixin

class Executeform(forms.Form,FormMixin):
        AlterID =forms.CharField(max_length=50)
        Hospital=forms.CharField(max_length=25)
        Executor=forms.CharField(max_length=50)
        ExecutionResult=forms.CharField(widget=forms.Textarea)

class updateExecuteForm(forms.Form,FormMixin):
        executeID=forms.IntegerField(required=True)
        AlterID =forms.CharField(max_length=50)
        Hospital=forms.CharField(max_length=25)
        Executor=forms.CharField(max_length=50)
        ExecutionResult=forms.CharField(widget=forms.Textarea)