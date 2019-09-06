# Generated by Django 2.2.1 on 2019-09-06 15:43

from django.db import migrations, models
import django.db.models.manager
import shortuuidfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, primary_key=True, serialize=False)),
                ('mobilephone', models.CharField(max_length=11, unique=True)),
                ('email', models.EmailField(max_length=254, null=True, unique=True)),
                ('worknumber', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('department', models.CharField(max_length=100)),
                ('userpermissions', models.CharField(max_length=4)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.',verbose_name='superuser status')),
                ('is_cancellation', models.BooleanField(default=False)),
                ('registrationtime', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'alt_user',
            },
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
    ]
