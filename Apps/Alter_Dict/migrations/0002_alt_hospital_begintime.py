# Generated by Django 2.2.1 on 2019-08-30 18:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Alter_Dict', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='alt_hospital',
            name='beginTime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]