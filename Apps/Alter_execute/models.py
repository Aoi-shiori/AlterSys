from django.db import models
from  shortuuidfield import ShortUUIDField
from Apps.Alter_Dict.models import Alt_Hospital
# Create your models here.
class Alter_execute(models.Model):
    id = models.AutoField(primary_key=True)#执行ID
    AlterID =models.CharField(max_length=50)#执行到的变更id
    Hospital=models.ForeignKey('Alter_Dict.Alt_Hospital', related_name='Hospital_datas', on_delete=models.SET_NULL, null=True)#'医院'#可通过db_column= 改变字段名
    Executor=models.CharField(max_length=50)#执行人
    ExecutionTime=models.DateTimeField(auto_now=True)#上次执行时间
    ExecutionResult=models.TextField(max_length=500)#执行结果记录
    UID=ShortUUIDField()
    Exports=models.CharField(max_length=255,null=True)
    class Meta:
        db_table = 'alt_execute'#执行表
