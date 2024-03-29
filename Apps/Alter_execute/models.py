from django.db import models
from  shortuuidfield import ShortUUIDField
from Apps.Alter_Dict.models import Alt_Hospital
# Create your models here.
class Alter_execute(models.Model):
    id = models.AutoField(primary_key=True)#执行ID
    userid = ShortUUIDField() #用户唯一ID
    alterid = models.CharField(max_length=50)#执行到的变更id
    #hospital=models.ForeignKey('Alter_Dict.Alt_Hospital', related_name='Hospital_datas', on_delete=models.SET_NULL, null=True)#'医院'#可通过db_column= 改变字段名
    hospitalid = models.CharField(max_length=5) #医院id
    databaseid = models.IntegerField() #数据库id
    executor = models.CharField(max_length=50)#执行人
    executiontime = models.DateTimeField(auto_now=True)#上次执行时间
    executionresult = models.CharField(max_length=500)#执行结果记录
    exportlist=models.CharField(max_length=1000, null=True) #已经导出列表记录
    class Meta:
        db_table = 'alt_execute'#执行表
