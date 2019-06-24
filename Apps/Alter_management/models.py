from django.db import models

# Create your models here.
class Alter_managment(models.Model):
        AlterID= models.AutoField(primary_key=True)#变更ID
        AlterType=models.CharField(max_length=100)#'关联类型BUG'#
        AssociatedNumber=models.CharField(max_length=50)#'关联编号'#
        Datebase=models.CharField(max_length=50)#'数据库'#
        AlterContent=models.TextField(max_length=1000) #变更内容
        Informant=models.CharField(max_length=50)# '填报人',
        FillTime=models.DateTimeField(auto_now=True)#'填报时间'
        Reviewer=models.CharField(max_length=50,null=True)# '审核人'
        ReviewStatus=models.CharField(max_length=2,null=True,default='0')#'审核状态',
        ReviewContent=models.TextField(max_length=1000,null=True)#'审核内容',
        AuditTime=models.DateTimeField(null=True)#'审核时间',

        class Meta:
            db_table='Alter_managment'