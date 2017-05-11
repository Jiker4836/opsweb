# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=11, null=True)),
            ],
            options={
                'db_table': 'department',
            },
        ),
        migrations.CreateModel(
            name='Idc',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=10, verbose_name=b'idc\xe5\xad\x97\xe6\xaf\x8d\xe7\xae\x80\xe7\xa7\xb0')),
                ('idc_name', models.CharField(max_length=100, verbose_name=b'idc\xe4\xb8\xad\xe6\x96\x87\xe5\x90\x8d')),
                ('address', models.CharField(max_length=255, verbose_name=b'idc\xe5\x9c\xb0\xe5\x9d\x80')),
                ('user', models.CharField(max_length=32, verbose_name=b'\xe6\x9c\xba\xe6\x88\xbf\xe8\x81\x94\xe7\xb3\xbb\xe4\xba\xba')),
                ('user_phone', models.CharField(max_length=20, verbose_name=b'\xe6\x9c\xba\xe6\x88\xbf\xe8\x81\x94\xe7\xb3\xbb\xe4\xba\xba\xe7\x94\xb5\xe8\xaf\x9d')),
                ('user_email', models.EmailField(max_length=20, verbose_name=b'\xe6\x9c\xba\xe6\x88\xbf\xe8\x81\x94\xe7\xb3\xbb\xe4\xba\xba\xe9\x82\xae\xe7\xae\xb1')),
            ],
            options={
                'db_table': 'idc',
                'permissions': (('view_idc', '\u67e5\u770bidc'),),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32, verbose_name=b'\xe4\xb8\x9a\xe5\x8a\xa1\xe7\xba\xbf\xe5\x90\x8d\xe7\xa7\xb0')),
                ('module_letter', models.CharField(max_length=32, verbose_name=b'\xe4\xb8\x9a\xe5\x8a\xa1\xe7\xba\xbf\xe5\xad\x97\xe6\xaf\x8d\xe7\xae\x80\xe7\xa7\xb0')),
                ('op_interface', models.CharField(max_length=255, verbose_name=b'\xe8\xbf\x90\xe7\xbb\xb4\xe8\xb4\x9f\xe8\xb4\xa3\xe4\xba\xba\xef\xbc\x9ausername1,username2')),
                ('dev_interface', models.CharField(max_length=255, verbose_name=b'\xe5\xbc\x80\xe5\x8f\x91\xe8\xb4\x9f\xe8\xb4\xa3\xe4\xba\xba\xef\xbc\x9ausername1,username2')),
                ('p_product', models.ForeignKey(verbose_name=b'\xe4\xb8\x8a\xe7\xba\xa7\xe4\xb8\x9a\xe5\x8a\xa1\xe7\xba\xbf', to='dashboard.Product', null=True)),
            ],
            options={
                'db_table': 'product',
                'permissions': (('view_product', '\u7ba1\u7406\u4e1a\u52a1\u7ebf'),),
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone', models.CharField(max_length=32, null=True)),
                ('title', models.CharField(max_length=32, null=True)),
                ('name', models.CharField(max_length=32, null=True, verbose_name=b'\xe4\xb8\xad\xe6\x96\x87\xe5\x90\x8d')),
                ('department', models.ForeignKey(to='dashboard.Department', null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_profile',
                'default_related_name': 'profile',
            },
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('supplier', models.IntegerField(null=True)),
                ('manufacturers', models.CharField(max_length=50, null=True)),
                ('manufacture_date', models.DateField(null=True)),
                ('server_type', models.CharField(max_length=20, null=True)),
                ('sn', models.CharField(max_length=60, null=True, db_index=True)),
                ('os', models.CharField(max_length=50, null=True)),
                ('hostname', models.CharField(max_length=50, null=True, db_index=True)),
                ('inner_ip', models.CharField(max_length=32, unique=True, null=True)),
                ('mac_address', models.CharField(max_length=50, null=True)),
                ('ip_info', models.CharField(max_length=255, null=True)),
                ('server_cpu', models.CharField(max_length=250, null=True)),
                ('server_disk', models.CharField(max_length=100, null=True)),
                ('server_mem', models.CharField(max_length=100, null=True)),
                ('status', models.CharField(max_length=100, null=True, db_index=True)),
                ('remark', models.TextField(null=True)),
                ('check_update_time', models.DateTimeField(auto_now=True, null=True)),
                ('vm_status', models.IntegerField(null=True, db_index=True)),
                ('uuid', models.CharField(max_length=100, null=True, db_index=True)),
                ('idc', models.ForeignKey(to='dashboard.Idc', null=True)),
            ],
            options={
                'db_table': 'server',
                'permissions': (('view_server', '\u8bbf\u95ee\u670d\u52a1\u5668\u4fe1\u606f'),),
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=32, verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81')),
            ],
            options={
                'db_table': 'status',
            },
        ),
    ]
