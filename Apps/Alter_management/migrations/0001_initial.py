# Generated by Django 2.2.1 on 2019-09-06 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alter_managment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('altertypeid', models.IntegerField(max_length=11)),
                ('associatedid', models.CharField(max_length=50)),
                ('databaseid', models.IntegerField(max_length=11)),
                ('altercontent', models.CharField(max_length=1000)),
                ('modifier', models.CharField(max_length=50)),
                ('modifytime', models.DateTimeField(auto_now=True)),
                ('reviewer', models.CharField(max_length=50, null=True)),
                ('reviewstatus', models.CharField(default='0', max_length=2, null=True)),
                ('reviewcontent', models.CharField(max_length=255, null=True)),
                ('reviewtime', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'alt_managment',
            },
        ),
        migrations.CreateModel(
            name='Alter_managment_checked',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('alterid', models.IntegerField(max_length=11)),
                ('altertypeid', models.IntegerField(max_length=11)),
                ('associatedid', models.CharField(max_length=50)),
                ('databaseid', models.IntegerField(max_length=11)),
                ('altercontent', models.CharField(max_length=5000)),
                ('modifier', models.CharField(max_length=50)),
                ('modifytime', models.DateTimeField(auto_now=True)),
                ('reviewer', models.CharField(max_length=50, null=True)),
                ('reviewstatus', models.CharField(default='0', max_length=2, null=True)),
                ('reviewcontent', models.CharField(max_length=1000, null=True)),
                ('reviewtime', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'alter_managment_checked',
            },
        ),
    ]
