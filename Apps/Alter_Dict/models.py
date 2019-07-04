from django.db import models

# Create your models here.
#数据库类型字典
class DBname(models.Model):
        Database=models.CharField(max_length=50)#数据库名称
        counts = models.CharField(max_length=50,null=True)
        class Meta:
                db_table='alt_db_dict'
#变更类型字典
class AltType(models.Model):
        AltType=models.CharField(max_length=50)
        class Meta:
                db_table='alt_type_dict'
