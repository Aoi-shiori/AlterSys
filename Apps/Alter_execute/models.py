from django.db import models

# Create your models here.
class Alter_execute(models.Model):
    executeID = models.AutoField(primary_key=True)
    AlterID =models.CharField(max_length=50)
    Hospital=models.CharField(max_length=25)
    Executor=models.CharField(max_length=50)
    ExecutionTime=models.DateTimeField(auto_now=True)
    ExecutionResult=models.CharField(max_length=255)
    class Meta:
        db_table = 'Alter_execute'
