from django.db import models

# Create your models here.
#数据库类型字典
class DBname(models.Model):
        Datebase=models.CharField(max_length=50)#数据库名称
        class Meta:
                db_table='alt_db_dict'
#变更类型字典
class AltType(models.Model):
        AltType=models.CharField(max_length=50)
        class Meta:
                db_table='alt_type_dict'
