# Generated by Django 2.2.1 on 2019-08-29 18:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Alter_execute', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alter_execute',
            name='Hospital',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Hospital_datas', to='Alter_Dict.Alt_Hospital'),
        ),
    ]