# Generated by Django 2.2.1 on 2019-07-11 03:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Alter_management', '0004_auto_20190704_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alter_managment',
            name='AltType',
            field=models.ForeignKey(db_column='AltType', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='AltType_datas', to='Alter_Dict.AltType'),
        ),
        migrations.AlterField(
            model_name='alter_managment',
            name='Database',
            field=models.ForeignKey(db_column='Database', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Database_datas', to='Alter_Dict.DBname'),
        ),
    ]
