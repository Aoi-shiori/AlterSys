from django.db import models

# Create your models here.
#数据库类型字典
class Alt_Database(models.Model):
        dbname=models.CharField(max_length=50)#数据库名称
        #classifycount = models.CharField(max_length=50,null=True) #使用该分类的数据量
        modifier =models.CharField(max_length=50) #修改人
        modifytime= models.DateTimeField(auto_now=True) #修改时间
        begintime= models.DateTimeField(auto_now_add=True) #创建时间
        # def __unicode__(self):
        #         return self.Database
        class Meta:
                db_table= 'alt_database_dict'
#变更类型字典
class Alt_Type(models.Model):
        altertypename=models.CharField(max_length=50)
        #classifycount = models.CharField(max_length=50, null=True) #使用该分类的数据量
        modifier =models.CharField(max_length=50) #修改人
        modifytime= models.DateTimeField(auto_now=True) #修改时间
        begintime= models.DateTimeField(auto_now_add=True) #创建时间

        # def __unicode__(self):
        #         return self.AltType
        class Meta:
                db_table='alt_type_dict'
#医院字典
class Alt_Hospital(models.Model):
        hospitalname=models.CharField(max_length=50)
        #classifycount = models.CharField(max_length=50, null=True)  # 使用该分类的数据量
        modifier =models.CharField(max_length=50) #修改人
        modifytime= models.DateTimeField(auto_now=True) #修改时间
        begintime= models.DateTimeField(auto_now_add=True) #创建时间

        # def __unicode__(self):
        #         return self.Hospital
        class Meta:
                db_table='alt_hospital_dict'
