# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ZtGroup(models.Model):
    name = models.CharField(max_length=30)
    role = models.CharField(max_length=30)
    desc = models.CharField(max_length=255)
    acl = models.TextField()

    class Meta:
        managed = False
        db_table = 'zt_group'


class ZtUser(models.Model):
    dept = models.PositiveIntegerField()
    account = models.CharField(unique=True, max_length=30)
    password = models.CharField(max_length=32)
    realname = models.CharField(max_length=100)
    role = models.CharField(max_length=10)
    nickname = models.CharField(max_length=60)
    commiter = models.CharField(max_length=100)
    avatar = models.CharField(max_length=30)
    birthday = models.DateField()
    gender = models.CharField(max_length=1)
    email = models.CharField(max_length=90)
    skype = models.CharField(max_length=90)
    qq = models.CharField(max_length=20)
    yahoo = models.CharField(max_length=90)
    gtalk = models.CharField(max_length=90)
    wangwang = models.CharField(max_length=90)
    mobile = models.CharField(max_length=11)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=120)
    zipcode = models.CharField(max_length=10)
    join = models.DateField()
    visits = models.PositiveIntegerField()
    ip = models.CharField(max_length=15)
    last = models.PositiveIntegerField()
    fails = models.IntegerField()
    locked = models.DateTimeField()
    ranzhi = models.CharField(max_length=30)
    score = models.IntegerField()
    scorelevel = models.IntegerField(db_column='scoreLevel')  # Field name made lowercase.
    deleted = models.CharField(max_length=1)
    status = models.CharField(max_length=7)

    class Meta:
        managed = False
        db_table = 'zt_user'
