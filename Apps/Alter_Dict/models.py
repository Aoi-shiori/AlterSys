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

#雲庫醫院字典表
class CtDepartment(models.Model):
    dept_id = models.CharField(db_column='DEPT_ID', primary_key=True, max_length=5)  # Field name made lowercase.
    dept_code = models.CharField(db_column='DEPT_CODE', max_length=20)  # Field name made lowercase.
    dept_name = models.CharField(db_column='DEPT_NAME', max_length=30)  # Field name made lowercase.
    branchcode = models.CharField(db_column='BranchCode', max_length=50)  # Field name made lowercase.
    branchname = models.CharField(db_column='BranchName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    superiorhos = models.CharField(db_column='SuperiorHos', max_length=6, blank=True, null=True)  # Field name made lowercase.
    dept_name_short = models.CharField(db_column='DEPT_NAME_SHORT', max_length=30, blank=True, null=True)  # Field name made lowercase.
    dept_des = models.CharField(db_column='DEPT_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    parent_id = models.CharField(db_column='PARENT_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    district_id = models.CharField(db_column='DISTRICT_ID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    kind = models.CharField(db_column='KIND', max_length=10, blank=True, null=True)  # Field name made lowercase.
    dept_level = models.IntegerField(db_column='DEPT_LEVEL')  # Field name made lowercase.
    final_flag = models.IntegerField(db_column='FINAL_FLAG', blank=True, null=True)  # Field name made lowercase.
    class_use_flag = models.CharField(db_column='CLASS_USE_FLAG', max_length=20, blank=True, null=True)  # Field name made lowercase.
    class_final_flag = models.CharField(db_column='CLASS_FINAL_FLAG', max_length=20, blank=True, null=True)  # Field name made lowercase.
    class_delete_flag = models.CharField(db_column='CLASS_DELETE_FLAG', max_length=20, blank=True, null=True)  # Field name made lowercase.
    quick_code1 = models.CharField(db_column='QUICK_CODE1', max_length=20, blank=True, null=True)  # Field name made lowercase.
    quick_code2 = models.CharField(db_column='QUICK_CODE2', max_length=30, blank=True, null=True)  # Field name made lowercase.
    quick_code3 = models.CharField(db_column='QUICK_CODE3', max_length=30, blank=True, null=True)  # Field name made lowercase.
    modified_by = models.CharField(db_column='MODIFIED_BY', max_length=40, blank=True, null=True)  # Field name made lowercase.
    modified_date = models.DateTimeField(db_column='MODIFIED_DATE', blank=True, null=True)  # Field name made lowercase.
    order_no = models.CharField(db_column='ORDER_NO', max_length=100, blank=True, null=True)  # Field name made lowercase.
    dept_address = models.CharField(db_column='DEPT_ADDRESS', max_length=50, blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=20, blank=True, null=True)  # Field name made lowercase.
    rank = models.CharField(db_column='Rank', max_length=20, blank=True, null=True)  # Field name made lowercase.
    intro = models.CharField(db_column='Intro', max_length=4000, blank=True, null=True)  # Field name made lowercase.
    guide = models.CharField(db_column='Guide', max_length=4000, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=100, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=20, blank=True, null=True)  # Field name made lowercase.
    logo = models.CharField(db_column='Logo', max_length=100, blank=True, null=True)  # Field name made lowercase.
    backpic = models.CharField(db_column='BackPic', max_length=100, blank=True, null=True)  # Field name made lowercase.
    longitude = models.CharField(db_column='Longitude', max_length=50, blank=True, null=True)  # Field name made lowercase.
    latitude = models.CharField(db_column='Latitude', max_length=50, blank=True, null=True)  # Field name made lowercase.
    isactive = models.IntegerField(db_column='IsActive', blank=True, null=True)  # Field name made lowercase.
    remarks = models.CharField(db_column='Remarks', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ct_department'
        unique_together = (('dept_id', 'branchcode'),)
