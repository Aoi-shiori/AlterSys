from django.db import models
from Apps.Alter_Dict.models import Alt_Database,Alt_Type

# Create your models here.
class Alter_managment(models.Model):
        id= models.AutoField(primary_key=True)#变更ID
        AltType=models.ForeignKey('Alter_Dict.Alt_Type', related_name='AltType_datas', on_delete=models.SET_NULL, null=True)#'关联类型BUG'#
        AssociatedNumber=models.CharField(max_length=50)#'关联编号'#
        Database=models.ForeignKey('Alter_Dict.Alt_Database', related_name='DBtype_datas', on_delete=models.SET_NULL, null=True)#'数据库'#
        AlterContent=models.TextField(max_length=1000) #变更内容
        Informant=models.CharField(max_length=50)# '填报人',
        FillTime=models.DateTimeField(auto_now=True)#'填报时间'
        Reviewer=models.CharField(max_length=50,null=True)# '审核人'
        ReviewStatus=models.CharField(max_length=2,null=True,default='0')#'审核状态',
        ReviewContent=models.TextField(max_length=1000,null=True)#'审核内容',
        AuditTime=models.DateTimeField(null=True)#'审核时间',


        class Meta:
            db_table='alt_managment'#变更表


class Alter_managment_checked(models.Model):
        id= models.AutoField(primary_key=True)#变更ID
        AltType=models.ForeignKey('Alter_Dict.Alt_Type', related_name='checked_AltType_datas', on_delete=models.SET_NULL, null=True)#'关联类型BUG'#可通过db_column= 改变字段名
        AssociatedNumber=models.CharField(max_length=50)#'关联编号'#
        Database=models.ForeignKey('Alter_Dict.Alt_Database', related_name='checked_Database_datas', on_delete=models.SET_NULL, null=True)#'数据库'#
        AlterContent=models.TextField(max_length=1000) #变更内容
        Informant=models.CharField(max_length=50)# '填报人',
        FillTime=models.DateTimeField(auto_now=True)#'填报时间'
        Reviewer=models.CharField(max_length=50,null=True)# '审核人'
        ReviewStatus=models.CharField(max_length=2,null=True,default='0')#'审核状态',
        ReviewContent=models.TextField(max_length=1000,null=True)#'审核内容',
        AuditTime=models.DateTimeField(null=True)#'审核时间',
        states=models.CharField(max_length=2,default='1')#状态字段


        class Meta:
            db_table='alter_managment_checked'#变更表
