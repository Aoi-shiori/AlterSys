from django.db import models
from Apps.Alter_Dict.models import Alt_Database,Alt_Type

# Create your models here.
class Alter_managment(models.Model):
        id= models.AutoField(primary_key=True)#变更ID
        #altertypenumber=models.ForeignKey('Alter_Dict.Alt_Type', related_name='AltType_datas', on_delete=models.SET_NULL, null=True)#'关联类型BUG'#
        altertypeid=models.IntegerField()
        associatedid=models.CharField(max_length=50)#'关联编号'#
        #dbnumber=models.ForeignKey('Alter_Dict.Alt_Database', related_name='DBtype_datas', on_delete=models.SET_NULL, null=True)#'数据库'#
        databaseid=models.IntegerField()
        altercontent=models.CharField(max_length=1000) #变更内容
        modifier=models.CharField(max_length=50)# '填报人',
        modifytime=models.DateTimeField(auto_now=True)#'填报时间'
        reviewer=models.CharField(max_length=50, null=True)# '审核人'
        reviewstatus=models.CharField(max_length=2, null=True, default='0')#'审核状态',
        reviewcontent=models.CharField(max_length=255, null=True)#'审核内容',
        reviewtime=models.DateTimeField(null=True)#'审核时间',


        class Meta:
            db_table='alt_managment'#变更表


class Alter_managment_checked(models.Model):
        id= models.AutoField(primary_key=True)#变更ID
        #alterid = models.ForeignKey('Alter_managment', on_delete=models.SET_NULL, null=True)
        alterid = models.IntegerField() #变更ID
        #alttypenumber=models.ForeignKey('Alter_Dict.Alt_Type', related_name='checked_AltType_datas', on_delete=models.SET_NULL, null=True,db_column='alttypenumber')#'关联类型BUG'#可通过db_column= 改变字段名
        altertypeid=models.IntegerField()
        associatedid=models.CharField(max_length=50)#'关联编号'#
        #dbnumber=models.ForeignKey('Alter_Dict.Alt_Database', related_name='checked_Database_datas', on_delete=models.SET_NULL, null=True,db_column='dbnumber')#'数据库'#
        databaseid=models.IntegerField()
        altercontent=models.CharField(max_length=5000) #变更内容
        modifier=models.CharField(max_length=50)# '填报人',
        modifytime=models.DateTimeField(auto_now=True)#'填报时间'
        reviewer=models.CharField(max_length=50, null=True)# '审核人'
        reviewstatus=models.CharField(max_length=2, null=True, default='0')#'审核状态',
        reviewcontent=models.CharField(max_length=1000, null=True)#'审核内容',
        reviewtime=models.DateTimeField(null=True)#'审核时间',

        class Meta:
            db_table='alter_managment_checked'#变更表
