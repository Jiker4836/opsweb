# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0021_auto_20170511_0803'),
    ]

    operations = [
        migrations.CreateModel(
            name='ZabbixHost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hostid', models.IntegerField(null=True, db_index=True)),
                ('host', models.CharField(max_length=50, null=True, db_index=True)),
                ('ip', models.CharField(max_length=50, null=True, db_index=True)),
                ('updatetime', models.DateTimeField(auto_now=True)),
                ('server', models.OneToOneField(null=True, to='dashboard.Server')),
            ],
            options={
                'db_table': 'resource_zabbix_cache',
            },
        ),
    ]
