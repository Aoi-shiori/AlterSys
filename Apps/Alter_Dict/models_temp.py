# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


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
