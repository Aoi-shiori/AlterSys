# Generated by Django 2.2.1 on 2019-09-12 14:25

from django.db import migrations
import shortuuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Alter_management', '0002_auto_20190908_1238'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='alter_managment',
            options={'permissions': (('review_alter_managment', '审核数据权限'),)},
        ),
        migrations.AddField(
            model_name='alter_managment',
            name='userid',
            field=shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22),
        ),
        migrations.AddField(
            model_name='alter_managment_checked',
            name='userid',
            field=shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22),
        ),
    ]
