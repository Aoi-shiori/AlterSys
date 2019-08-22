from django.db import models
from  shortuuidfield import ShortUUIDField

# Create your models here.
class Alter_execute(models.Model):
    id = models.AutoField(primary_key=True)#执行ID
    AlterID =models.CharField(max_length=50)#执行到的变更id
    Hospital=models.CharField(max_length=25)#医院
    Executor=models.CharField(max_length=50)#执行人
    ExecutionTime=models.DateTimeField(auto_now=True)#上次执行时间
    ExecutionResult=models.TextField(max_length=500)#执行结果记录
    UID=ShortUUIDField(unique=True)
    class Meta:
        db_table = 'alt_execute'#执行表
