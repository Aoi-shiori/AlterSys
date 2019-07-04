from django.db import models
from Apps.Alter_Dict.models import DBname,AltType

# Create your models here.
class Alter_managment(models.Model):
        id= models.AutoField(primary_key=True)#变更ID
        AltType=models.ForeignKey('Alter_Dict.AltType',on_delete=models.SET_NULL,null=True,db_column='AltType')#'关联类型BUG'#
        AssociatedNumber=models.CharField(max_length=50)#'关联编号'#
        Database=models.ForeignKey('Alter_Dict.DBname',on_delete=models.SET_NULL,null=True,db_column='Database')#'数据库'#
        AlterContent=models.TextField(max_length=1000) #变更内容
        Informant=models.CharField(max_length=50)# '填报人',
        FillTime=models.DateTimeField(auto_now=True)#'填报时间'
        Reviewer=models.CharField(max_length=50,null=True)# '审核人'
        ReviewStatus=models.CharField(max_length=2,null=True,default='0')#'审核状态',
        ReviewContent=models.TextField(max_length=1000,null=True)#'审核内容',
        AuditTime=models.DateTimeField(null=True)#'审核时间',
        Expstatus=models.BooleanField(default=False)#导出状态，已经导出过置为true


        class Meta:
            db_table='alt_managment'#变更表

