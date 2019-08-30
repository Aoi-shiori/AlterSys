from django.db import models

# Create your models here.
#数据库类型字典
class Alt_Database(models.Model):
        Database=models.CharField(max_length=50)#数据库名称
        counts = models.CharField(max_length=50,null=True)
        # def __unicode__(self):
        #         return self.Database
        class Meta:
                db_table= 'alt_database_dict'
#变更类型字典
class Alt_Type(models.Model):
        AltType=models.CharField(max_length=50)
        counts = models.CharField(max_length=50, null=True)
        # def __unicode__(self):
        #         return self.AltType
        class Meta:
                db_table='alt_type_dict'
#医院字典
class Alt_Hospital(models.Model):
        Hospital=models.CharField(max_length=50)
        beginTime= models.DateTimeField(auto_now_add=True)
        counts = models.CharField(max_length=50, null=True)
        # def __unicode__(self):
        #         return self.Hospital
        class Meta:
                db_table='alt_hospital_dict'
